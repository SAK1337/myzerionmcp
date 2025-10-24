# listGasPrices Tool Documentation

## Overview
The `listGasPrices` tool provides real-time information on current gas prices across all supported blockchain networks.

## Endpoint
```
GET /v1/gas-prices/
```

## Parameters

### Optional Query Parameters

1. **`filter[chain_ids]`** (array of strings)
   - Description: Return only gas prices from specified chains
   - Format: Comma-separated array
   - Example: `["ethereum", "polygon", "arbitrum"]`
   - Find available chain IDs using the `listChains` tool

2. **`filter[gas_types]`** (array of strings)
   - Description: Return only gas prices with specified gas-type
   - Format: Comma-separated array
   - Valid values: 
     - `classic` - Traditional gas pricing
     - `eip1559` - EIP-1559 gas pricing (base fee + priority fee)
     - `optimistic` - Optimistic rollup gas pricing

## MCP Tool Call Example

### Get all gas prices (no filters)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "listGasPrices",
    "arguments": {}
  }
}
```

### Get gas prices for specific chains
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "listGasPrices",
    "arguments": {
      "filter[chain_ids]": ["ethereum", "polygon"]
    }
  }
}
```

## Response Format

The tool returns gas price information for the requested chains, including:
- Chain identifier
- Gas prices for different priority levels (slow, normal, fast)
- Timestamp of the data
- Additional chain-specific gas pricing details

## Use Cases

1. **Transaction Fee Estimation**: Get current gas prices to estimate transaction costs
2. **Multi-chain Comparison**: Compare gas prices across different blockchains
3. **Optimal Timing**: Monitor gas prices to execute transactions during low-fee periods
4. **DApp Integration**: Display real-time gas prices to users in your application

## Notes

- Gas prices fluctuate frequently based on network demand
- Response times are optimized for real-time data
- Requires valid Zerion API key in configuration
- Returns 401 if authentication fails
- Returns 429 if rate limit is exceeded
