#!/usr/bin/env python3
"""Test script to call the listGasPrices MCP tool."""

import asyncio
import httpx

async def test_list_gas_prices():
    """Test the listGasPrices tool."""
    
    # MCP tool call format
    tool_call = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "listGasPrices",
            "arguments": {}
        }
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Call the MCP server
            response = await client.post(
                "http://127.0.0.1:8000/mcp/v1",
                json=tool_call,
                timeout=30.0
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response:")
            print(response.text[:2000])  # Print first 2000 chars
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_list_gas_prices())
