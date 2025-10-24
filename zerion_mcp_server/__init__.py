#!/usr/bin/env python3
"""Universal MCP Server for OpenAPI specifications."""

import time
import yaml
import httpx
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType

from .config import ConfigManager
from .errors import ConfigError, NetworkError, APIError, ValidationError
from .logger import setup_logging, get_logger


def main(transport: str = "stdio"):
    """Main entry point.
    
    Args:
        transport: Transport mode - 'stdio' (default) or 'http'
    """
    # Load configuration
    try:
        config = ConfigManager()
    except ConfigError as e:
        print(f"Configuration error: {e}")
        return
    
    # Setup logging
    setup_logging(level=config.log_level, format_type=config.log_format)
    logger = get_logger(__name__)
    
    logger.info("Starting Zerion MCP Server")
    logger.info(f"Configuration loaded", extra={
        "config_source": "config.yaml" if config.get("_config_loaded_from_file") else "defaults",
        "base_url": config.base_url,
        "log_level": config.log_level,
        "log_format": config.log_format
    })
    
    # Download OpenAPI spec (YAML format)
    logger.info(f"Loading OpenAPI specification from {config.oas_url}")
    start_time = time.time()
    
    try:
        if config.oas_url.startswith(("http://", "https://")):
            response = httpx.get(config.oas_url, timeout=30.0)
            response.raise_for_status()
            spec_content = response.text
        else:
            with open(config.oas_url, "r", encoding="utf-8") as f:
                spec_content = f.read()

        spec_size = len(spec_content)
        openapi_spec = yaml.safe_load(spec_content)
        
        load_duration = time.time() - start_time
        logger.info("OpenAPI specification loaded successfully", extra={
            "duration_sec": round(load_duration, 2),
            "spec_size_bytes": spec_size,
            "endpoints": len(openapi_spec.get("paths", {}))
        })
        
    except httpx.TimeoutException as e:
        error = NetworkError(
            f"Timeout loading OpenAPI specification",
            url=config.oas_url,
            timeout=30.0,
            context={"suggestion": "Check your internet connection"}
        )
        logger.error(str(error), extra=error.context)
        print(f"Error: {error}")
        return
    except httpx.HTTPStatusError as e:
        error = APIError.from_response(
            e.response,
            message=f"Failed to download OpenAPI spec from {config.oas_url}"
        )
        logger.error(str(error), extra=error.context)
        print(f"Error: {error}")
        return
    except yaml.YAMLError as e:
        error = ValidationError(
            f"Invalid YAML in OpenAPI specification: {e}",
            context={"suggestion": "Check the OpenAPI spec file format"}
        )
        logger.error(str(error), extra=error.context)
        print(f"Error: {error}")
        return
    except Exception as e:
        logger.error(f"Unexpected error loading OpenAPI spec", extra={"error": str(e)}, exc_info=True)
        print(f"Error loading OpenAPI spec from {config.oas_url}: {e}")
        return
    
    # Setup headers (API key from config)
    headers = {"Authorization": config.api_key}
    logger.debug("HTTP client configured", extra={"base_url": config.base_url})
    
    # Create HTTP client
    client = httpx.AsyncClient(
        base_url=config.base_url,
        headers=headers,
        timeout=30.0
    )
    
    # Create MCP server
    try:
        logger.info("Creating MCP server from OpenAPI spec")
        mcp = FastMCP.from_openapi(
            openapi_spec=openapi_spec,
            client=client,
            name=config.name,
            route_maps=[RouteMap(mcp_type=MCPType.TOOL)]
        )
        
        # Count tools
        tool_count = len([r for r in (openapi_spec.get("paths", {}) or [])])
        logger.info("MCP server created successfully", extra={
            "server_name": config.name,
            "tools_available": tool_count
        })
        
    except Exception as e:
        logger.error("Failed to create MCP server", extra={"error": str(e)}, exc_info=True)
        print(f"Error creating MCP server: {e}")
        return
    
    # Start server with requested transport
    logger.info("Server started and ready to accept requests")
    
    if transport == "http":
        # Run HTTP server for testing
        import uvicorn
        from starlette.applications import Starlette
        from starlette.responses import JSONResponse
        from starlette.routing import Route
        
        async def handle_mcp_request(request):
            """Handle MCP JSON-RPC requests over HTTP."""
            try:
                body = await request.json()
                method = body.get("method")
                params = body.get("params", {})
                request_id = body.get("id")
                
                logger.debug(f"MCP Request: {method}", extra={"params": params})
                
                # Handle different MCP methods
                if method == "tools/call":
                    tool_name = params.get("name")
                    tool_args = params.get("arguments", {})
                    
                    # Call the tool through FastMCP's internal mechanism
                    try:
                        # Use the correct method from FastMCPOpenAPI
                        result = await mcp._mcp_call_tool(tool_name, tool_args)
                        
                        # Format response according to MCP spec
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": result if isinstance(result, dict) else {"content": [{"type": "text", "text": str(result)}]}
                        })
                    except Exception as tool_error:
                        logger.error(f"Tool call error: {tool_error}", exc_info=True)
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {"code": -32603, "message": f"Tool execution error: {str(tool_error)}"}
                        }, status_code=500)
                
                elif method == "tools/list":
                    # List available tools through MCP server
                    try:
                        result = await mcp._mcp_list_tools()
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": result if isinstance(result, dict) else {"tools": result}
                        })
                    except Exception as list_error:
                        logger.error(f"List tools error: {list_error}", exc_info=True)
                        return JSONResponse({
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {"tools": []}
                        })
                
                else:
                    return JSONResponse({
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32601, "message": f"Method not found: {method}"}
                    }, status_code=404)
                    
            except Exception as e:
                logger.error(f"Request error: {e}", exc_info=True)
                return JSONResponse(
                    {"jsonrpc": "2.0", "id": body.get("id") if 'body' in locals() else None, "error": {"code": -32603, "message": str(e)}},
                    status_code=500
                )
        
        async def debug_mcp(request):
            """Debug endpoint to inspect MCP object."""
            attrs = {
                "type": str(type(mcp)),
                "attributes": [attr for attr in dir(mcp) if not attr.startswith('__')],
                "has_server": hasattr(mcp, '_server'),
                "has_tools": hasattr(mcp, '_tools'),
                "mcp_class": mcp.__class__.__name__
            }
            return JSONResponse(attrs)
        
        app = Starlette(routes=[
            Route("/mcp/v1", handle_mcp_request, methods=["POST"]),
            Route("/debug", debug_mcp, methods=["GET"])
        ])
        logger.info("Starting HTTP server on http://127.0.0.1:8000")
        logger.info("Debug endpoint available at http://127.0.0.1:8000/debug")
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    else:
        # Run stdio transport (default MCP mode)
        mcp.run()


if __name__ == "__main__":
    main()
