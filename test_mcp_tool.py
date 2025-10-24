#!/usr/bin/env python3
"""Test MCP server tools via stdio."""

import json
import subprocess
import sys

def send_request(proc, request):
    """Send a JSON-RPC request to the MCP server."""
    request_str = json.dumps(request) + "\n"
    proc.stdin.write(request_str.encode())
    proc.stdin.flush()
    
    # Read response
    response_line = proc.stdout.readline().decode().strip()
    if response_line:
        return json.loads(response_line)
    return None

def main():
    """Test the listGasPrices tool."""
    
    # Start the MCP server
    proc = subprocess.Popen(
        [r".venv\Scripts\python.exe", "-m", "zerion_mcp_server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=r"c:\temp\myzerionmcp"
    )
    
    try:
        # Initialize the MCP connection
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        print("Sending initialize request...")
        response = send_request(proc, init_request)
        print(f"Initialize response: {json.dumps(response, indent=2)}\n")
        
        # List available tools
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        print("Listing tools...")
        response = send_request(proc, list_tools_request)
        print(f"Tools list response:")
        if response and "result" in response:
            tools = response["result"].get("tools", [])
            print(f"Found {len(tools)} tools:")
            for tool in tools[:5]:  # Show first 5
                print(f"  - {tool.get('name')}: {tool.get('description', 'No description')[:80]}")
        print()
        
        # Call listGasPrices tool
        call_tool_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "listGasPrices",
                "arguments": {}
            }
        }
        
        print("Calling listGasPrices tool...")
        response = send_request(proc, call_tool_request)
        print(f"listGasPrices response:")
        print(json.dumps(response, indent=2)[:1000])
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        stderr_output = proc.stderr.read().decode()
        if stderr_output:
            print(f"Server stderr: {stderr_output}", file=sys.stderr)
    finally:
        proc.terminate()
        proc.wait(timeout=5)

if __name__ == "__main__":
    main()
