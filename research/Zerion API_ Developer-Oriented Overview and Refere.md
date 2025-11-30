<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Zerion API: Developer-Oriented Overview and Reference

The Zerion API is a **REST wallet data API** that aggregates and normalizes on‑chain data (balances, DeFi positions, NFTs, transactions, PnL) across EVM chains and Solana, behind a unified schema. It is designed for building wallets, portfolio trackers, analytics dashboards, agents, and alerting systems without running your own indexers or nodes.[^1][^2][^3][^4][^5]

Below is a developer‑focused “mini‑docs” that covers:

- What the API does and core concepts
- Authentication, base URL, environments
- Main endpoint groups and methods
- Request parameters and filters (per endpoint)
- Response structure and concrete JSON examples
- Webhooks / `tx-subscriptions`
- Errors, rate limits, and best practices

***

## 1. High‑Level Capabilities

Zerion’s API exposes on‑chain portfolio data via a small set of high‑value endpoints:[^2][^6][^3][^1]

- **Wallet portfolio** (net worth, allocation, PnL, per‑chain breakdown)
- **Token \& DeFi positions** (wallet balances plus LPs, staking, lending, rewards)[^7]
- **NFT portfolio \& positions** (collections, items, prices, metadata)[^8][^9][^10][^11]
- **Transactions** (normalized, decoded multi‑chain history)[^12][^13]
- **Charts / PnL** (historical balance charts and profit/loss)[^14][^15]
- **Webhooks** (`tx-subscriptions` for real‑time transaction alerts on EVM + Solana)[^4][^16]
- **Metadata \& chains** (supported chains and IDs)[^17][^10]

A single wallet query can cover **all supported EVM chains and Solana** in one response, with unified schemas for tokens, NFTs, transactions, and DeFi positions.[^6][^3][^1][^2][^4]

***

## 2. Authentication, Base URL \& Environments

### Base URL

All examples and docs use:

```text
https://api.zerion.io/
```

Versioned paths are under `/v1/...` (e.g. `/v1/wallets/{address}/transactions/`).[^13][^12][^7]

### Authentication

Zerion uses **HTTP Basic Auth** with the API key as username and no password:[^18]

```http
Authorization: Basic <base64(api_key + ":")>
```

In cURL, the docs and blog posts show this directly in the header:[^16][^4][^12][^13]

```bash
curl --request GET \
  --url 'https://api.zerion.io/v1/wallets/{address}/transactions/?currency=usd&page[size]=100&filter[trash]=no_filter' \
  --header 'accept: application/json' \
  --header 'authorization: Basic <BASE64_KEY>'
```

Key points:

- Put the API key in the **username** position of HTTP Basic auth.
- No password is required.[^18]
- Always send `Accept: application/json`.


### Rate limits \& plans

Public marketing pages describe a **Developer / free tier** and higher‑volume paid tiers:[^10][^1]

- Free/dev keys: a few **thousand requests/day**, low RPS, intended for local dev \& MVPs.[^1][^10]
- Production keys: significantly higher RPS (up to **~150 RPS by default**, higher on request for enterprise).[^1]
- Rate‑limit details and usage are visible in the Zerion dashboard.[^10][^1]

Exact quotas change over time; check your account dashboard for current numbers.

### Mainnet vs testnets

Several endpoint docs mention **testnet support using an `X-Env` header**:[^19][^9][^8]

```http
X-Env: test
```

or similar (naming can vary; check the latest reference). With this header set, the same endpoints can return data from supported test networks.

***

## 3. Data Model \& Response Structure

Zerion uses a JSON:API‑style structure across endpoints:[^4][^12]

- **Top‑level fields**:
    - `data`: a single resource object or an array
    - `included`: related objects (chains, fungibles, protocols, collections, etc.)
    - `links`: pagination (e.g. `self`, `next`)
- **Resource object**:
    - `type`: e.g. `"transactions"`, `"positions"`, `"nft-positions"`
    - `id`: Zerion’s stable internal ID for that object
    - `attributes`: core domain data for the resource
    - `relationships`: references to other resources whose full objects appear in `included`

Example: truncated **transactions** response from the docs/blog:[^12]

```json
{
  "links": {
    "self": "https://api.zerion.io/v1/wallets/0x.../transactions/?currency=usd&filter%5Bchain_ids%5D=base%2Cethereum&filter%5Btrash%5D=no_filter&page%5Bafter%5D=WyIiLCIiXQ%3D%3D&page%5Bsize%5D=100",
    "next": "https://api.zerion.io/v1/wallets/0x.../transactions/?currency=usd&filter%5Bchain_ids%5D=base%2Cethereum&filter%5Btrash%5D=no_filter&page%5Bafter%5D=WyIyMDI1LTA2LTA0VDIwOjUzOjExWiIsImU0NTkyNjg0MGE2NzVhY2ViYTIyNTM2MjU4YjRiMjM5Il0%3D&page%5Bsize%5D=100"
  },
  "data": [
    {
      "type": "transactions",
      "id": "f81256210272589b9d3fe717864417e4",
      "attributes": {
        "operation_type": "execute",
        "hash": "0x550a77...",
        "mined_at_block": 22823677,
        "mined_at": "2025-07-01T10:04:47Z",
        "sent_from": "0x42b9df65b2...",
        "sent_to": "0x663dc15d3c...",
        "status": "confirmed",
        "nonce": 5443,
        "fee": {
          "fungible_info": {
            "name": "Ethereum",
            "symbol": "ETH",
            "icon": { "url": "https://cdn.zerion.io/eth.png" },
            "flags": { "verified": true }
          },
          "quantity": { "...": "..." },
          "price":  ...,
          "value":  ...
        },
        "transfers": [ /* per‑asset in/out transfers */ ],
        "flags": { "is_trash": false },
        "application_metadata": { /* dapp/protocol info, if applicable */ }
      },
      "relationships": {
        "chain": { "data": { "type": "chains", "id": "base" } },
        "dapp": { "data": { "type": "dapps", "id": "some-dapp-id" } }
      }
    }
  ],
  "included": [
    /* optional related chains, fungibles, dapps, etc. */
  ]
}
```

The same schema is reused for both EVM and Solana transactions, including in Solana webhook payloads.[^4]

***

## 4. Wallet Endpoints

All wallet endpoints live under:

```text
/v1/wallets/{address}/...
```

They power portfolio trackers and wallets, including Zerion’s own app and partners like Rainbow, Infinex, and others.[^20][^21][^7]

### 4.1 Get Wallet Portfolio (summary)

**Purpose:** Overall portfolio overview for a wallet – total value, allocation, and key metrics across all supported chains.[^22][^2][^7]

**Endpoint:**

```http
GET /v1/wallets/{address}/portfolio
```

Typical query params (from wrappers \& docs references):[^23][^22][^7]

- `currency`: fiat/crypto currency code, e.g. `usd`, `eur`, `eth`, `btc`
- `filter[chain_ids]`: comma‑separated list of chains (e.g. `ethereum,base,optimism`)
- `filter[asset_types]`: filter by fungible / NFT / DeFi types
- `filter[trash]`: `only_non_trash`, `only_trash`, `no_filter`
- Pagination fields (if the portfolio resource is paginated by sub‑sections)

**Responses:**

- `200 OK`: `data` with a `portfolio` resource, containing:
    - Total value in requested currency
    - Per‑chain breakdown
    - Per‑asset‑type breakdown (tokens, NFTs, DeFi)
    - PnL and cost basis aggregates
- `202 Accepted`: portfolio is being prepared for a newly seen address; client should retry later.[^23]

The GitHub TS wrapper notes the `202` behavior for several wallet endpoints and advises polling until `200`.[^23]

***

### 4.2 Get Wallet Positions (tokens + DeFi)

**Purpose:** All **fungible positions** for a wallet, across all chains – including simple token balances and DeFi positions (lending, staking, LPs, rewards, etc.).[^2][^7][^23]

**Endpoint:**

```http
GET /v1/wallets/{address}/positions/
```

**Key query parameters** (from the wrapper \& blog on DeFi positions):[^7][^23]

- `currency`: price currency, e.g. `usd`
- `filter[position_types]`: subset of
`deposit | loan | locked | staked | reward | wallet | airdrop | margin`
- `filter[positions]`:
    - `only_complex` – returns only DeFi protocol positions (lending, LPs, staking etc.)[^7]
    - default – includes both simple token balances and complex positions
- `filter[protocol_ids]`: comma‑separated dapp/protocol IDs
- `filter[chain_ids]`: comma‑separated chain IDs (e.g. `ethereum,base,arbitrum`)[^7]
- `filter[fungible_ids]`: restrict by specific fungible tokens
- `filter[trash]`: hide spam/ignored assets (`only_non_trash`)[^7]
- `sort`: sort by fields such as `value` (descending), `name`, etc.[^23][^7]
- Pagination: `page[after]`, `page[size]` (cursor‑based)[^23]

**Example request (DeFi‑only positions):**[^7]

```bash
curl --request GET \
  --url 'https://api.zerion.io/v1/wallets/0x42b9df65b219b3dd36ff330a4dd8f327a6ada990/positions/?filter[positions]=only_complex&currency=usd&filter[trash]=only_non_trash&sort=value' \
  --header 'accept: application/json' \
  --header 'authorization: Basic <BASE64_KEY>'
```

**Response shape:**

- Each item in `data`:
    - `type`: `"positions"`
    - `id`: position ID
    - `attributes`:
        - `position_type` (e.g. `wallet`, `deposit`, `loan`, `staked`, `reward`)[^23][^7]
        - `quantity` (int/float/decimals) for the underlying asset
        - `value` and `price` in requested currency
        - `flags` including `is_trash`
        - Protocol‑specific breakdown for DeFi positions (e.g., per‑token composition of LP shares)[^7]
    - `relationships`:
        - `chain`
        - `fungible` (the token)
        - `protocol` / `dapp` (for DeFi LPs, lending, staking, etc.)
- `included` typically contains referenced `chains`, `fungibles`, and `dapps`.[^23][^7]

**Special behavior:**

- `202 Accepted` if the wallet has not been indexed yet.[^23]

***

### 4.3 Get Wallet NFT Portfolio \& Positions

Zerion distinguishes **NFT portfolio overview**, **NFT positions**, and **NFT collections**.[^9][^11][^8][^10]

#### 4.3.1 NFT portfolio overview

**Purpose:** High‑level summary of a wallet’s NFT holdings, analogous to the fungible portfolio but for NFTs only.[^11][^10]

**Endpoint:**

```http
GET /v1/wallets/{address}/nft-portfolio
```

**Typical params:**

- `currency`
- `filter[chain_ids]`
- `filter[trash]`

**Response:**

- A portfolio resource summarizing:
    - Total NFT value
    - Value per chain
    - Distribution by collection


#### 4.3.2 NFT positions (per‑token positions)

**Purpose:** Detailed list of each NFT token position (per collection, per token ID etc.).[^9][^23]

**Endpoint:**

```http
GET /v1/wallets/{address}/nft-positions
```

**Key query parameters** (from the TS wrapper \& docs snippets):[^8][^9][^23]

- `currency`
- `filter[chain_ids]`
- `filter[collections_ids]`: restrict to specific NFT collections
- `filter[trash]`
- `sort`: e.g. by collection name, value
- `include`: comma‑separated related resource types to include (e.g. `collections`)[^23]
- Pagination: `page[after]`, `page[size]`

**Response:**

- `data` array of `"nft-positions"` objects:
    - `attributes`:
        - `quantity` (for ERC‑1155, may be >1)
        - `token_id`, `name`, `description`
        - `image` / media URLs
        - `floor_price`, `estimated_value` (where available)[^10]
    - `relationships`:
        - `collection`
        - `chain`
- `included` often has NFT `collections` and `chains`.

As with other wallet endpoints, `202 Accepted` can be returned for a newly seen wallet.[^8][^23]

#### 4.3.3 NFT collections

**Purpose:** Aggregate per‑collection data for collections held by the wallet (floor price, count, etc.).[^8]

**Endpoint:**

```http
GET /v1/wallets/{address}/nft-collections
```

**Response:** `data` array of `"nft-collections"` with attributes such as collection name, slug, floor price, number of items held, and relationships to the chain and collection metadata object.[^10][^8]

***

### 4.4 Get Wallet Transactions

**Purpose:** Unified transaction history across **50+ chains** in a single feed, with decoded operation types and per‑asset transfers.[^24][^3][^13][^12]

**Endpoint:**

```http
GET /v1/wallets/{address}/transactions/
```

**Core query parameters** (from docs/blog examples):[^13][^12]

- `currency`: e.g. `usd`
- `page[size]`: page size (e.g. `100`)
- `page[after]`: cursor for next page (from `links.next`)
- `filter[chain_ids]`: e.g. `ethereum,base` for cross‑chain filtering[^12][^13]
- `filter[asset_types]`: (omitted in examples; supports asset‑type filtering where needed)[^12]
- `filter[trash]`: `no_filter`, `only_non_trash`, etc.[^13][^12]
- `filter[operation_types]`: restrict to `trade`, `transfer`, `execute`, etc. (available in the OpenAPI spec and wrappers)[^15][^23]

**Example: all L2 transactions:**[^13]

```bash
curl --request GET \
  --url 'https://api.zerion.io/v1/wallets/0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990/transactions/?currency=usd&page[size]=100&filter[trash]=no_filter' \
  --header 'accept: application/json' \
  --header 'authorization: Basic <BASE64_KEY>'
```

**Example: Ethereum + Base only:**[^12][^13]

```bash
curl --request GET \
  --url 'https://api.zerion.io/v1/wallets/0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990/transactions/?currency=usd&page[size]=100&filter[asset_types]=&filter[chain_ids]=ethereum,base&filter[trash]=no_filter' \
  --header 'accept: application/json' \
  --header 'authorization: Basic <BASE64_KEY>'
```

**Response (per transaction)** – from examples and Solana webhook schema:[^4][^13][^12]

- `attributes`:
    - `operation_type`: e.g. `trade`, `transfer`, `execute`
    - `hash`: tx hash (EVM) or signature (Solana)
    - `status`: `confirmed`, `failed`, etc.
    - `mined_at_block` and `mined_at` (timestamp)
    - `sent_from`, `sent_to`
    - `nonce`
    - `fee`:
        - `fungible_info`: token used for fees (ETH, SOL, etc.), including:
            - `name`, `symbol`, `icon.url`, `flags.verified`, `implementations` (per chain address/decimals)[^4][^12]
        - `quantity`: `{decimals, float, int, numeric}`
        - `price` (in requested currency)
        - `value` (fee * price)
    - `transfers`: array of in/out transfers per asset:
        - `direction`: `in` or `out`
        - `fungible_info` (or NFT info)
        - `quantity`, `price`, `value`
        - `sender`, `recipient`
        - `act_id`: links to a particular “act” in the transaction[^4]
    - `application_metadata` for the protocol/dapp (icon, name, contract address)[^13][^4]
    - `flags.is_trash` to mark spam / dust transfers[^12][^4]
- `relationships`:
    - `chain` (e.g. `"chain_id": "base"` or `"solana"`)[^4][^12]
    - `dapp` (e.g. `Jupiter` on Solana)[^4]

***

### 4.5 Wallet Balance Chart (Time Series)

**Purpose:** Historical portfolio value over time (balances chart), often used to render PnL graphs in UI.[^14][^15]

**Endpoint:**

```http
GET /v1/wallets/{address}/chart
```

**Parameters** (from docs snippets \& OpenAPI spec):[^15][^14]

- `currency`
- `filter[chain_ids]`
- `filter[asset_types]`: optionally focus on certain asset groups
- Time range options (e.g. `period`, timestamps, or number of points – see current docs)

**Response:**

- `data` with an array of time series points:
    - Each point includes timestamp and portfolio value in requested currency.
- Used to build cumulative PnL or balance charts.

***

## 5. Webhooks: `tx-subscriptions` (EVM + Solana)

Zerion exposes a **webhook‑based subscription system** to get push notifications whenever specified addresses transact on supported chains (EVM and Solana).[^16][^13][^12][^4]

### 5.1 Create a transaction subscription

**Endpoint:**

```http
POST /v1/tx-subscriptions
```

**Body:**

- `addresses`: array of wallet addresses to monitor (EVM or Solana)[^16][^4]
- `callback_url`: HTTPS endpoint that will receive POST webhook events[^16][^4]
- `chain_ids`: optional array of chain IDs to restrict scope. If omitted, subscription may cover all supported chains for that address.[^16][^4]

**Example (EVM – Base):**[^16]

```bash
curl --request POST \
  --url https://api.zerion.io/v1/tx-subscriptions \
  --header 'accept: application/json' \
  --header 'authorization: Basic <BASE64_KEY>' \
  --header 'content-type: application/json' \
  --data '{
    "addresses": ["0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990"],
    "callback_url": "https://webhook.site/dd3c5376-2472-4b3f-af38-d75cc20ad1a2",
    "chain_ids": ["base"]
  }'
```

**Example (Solana):**[^4]

```bash
curl --request POST \
  --url https://api.zerion.io/v1/tx-subscriptions/ \
  --header 'accept: application/json' \
  --header 'authorization: Basic <BASE64_KEY>' \
  --header 'content-type: application/json' \
  --data '{
    "addresses": ["8BH9pjtgyZDC4iAQH5ZiYDZ1MDWC98xki2V8NzqqKW3K"],
    "callback_url": "https://webhook.site/a1197f43-1522-4689-bbbb-5e7dcc3b346e",
    "chain_ids": ["solana"]
  }'
```

**Response (subscription creation):**[^4]

- `data` object, type `"callback"` or `"tx-subscriptions"` depending on context:
    - `attributes`:
        - `address`
        - `callback_url`
        - `timestamp` (created at)
    - `id`: callback or subscription ID
    - `relationships.subscription.data.id`: the subscription ID (type `"tx-subscriptions"`)

Use this ID to manage the subscription later (enable/disable, patch addresses, etc.).[^4]

### 5.2 Webhook payload schema

When a subscribed address has a new transaction:

- Zerion sends a **signed POST** to `callback_url`.[^4]
- The payload follows the **same `transactions` schema** as the REST `wallets/{address}/transactions` endpoint, plus callback metadata.

Example (truncated, Solana):[^4]

```json
{
  "data": {
    "type": "callback",
    "id": "bf300927-3f57-4d00-a01a-f7b75bd9b8de",
    "attributes": {
      "address": "8BH9pjtgyZDC4iAQH5ZiYDZ1MDWC98xki2V8NzqqKW3K",
      "callback_url": "https://webhook.site/a1197f43-1522-4689-bbbb-5e7dcc3b346e",
      "timestamp": "2025-10-16T10:56:50.047643374Z"
    },
    "relationships": {
      "subscription": {
        "id": "61f13641-443e-4068-932b-c28edeaefd85",
        "type": "tx-subscriptions"
      }
    }
  },
  "included": [
    {
      "type": "transactions",
      "id": "13de850a-bfa4-54c7-a7bb-fd6371d98894",
      "attributes": {
        "operation_type": "trade",
        "hash": "i5hptq3Dx8mbuAY5SuF5mUz7mTrAQYmwrJSrdUC4L1MJEkxsXDgSVt9to6HU8EcNygoLnhD7ut11r3mAQafP6Gx",
        "mined_at": "2025-10-16T10:56:48Z",
        "mined_at_block": 0,
        "sent_from": "8BH9pjtgyZDC4iAQH5ZiYDZ1MDWC98xki2V8NzqqKW3K",
        "sent_to": "",
        "status": "confirmed",
        "fee": {
          "fungible_info": {
            "name": "Solana",
            "symbol": "SOL",
            "icon": { "url": "https://cdn.zerion.io/11111111111111111111111111111111.png" },
            "flags": { "verified": true },
            "implementations": [
              {
                "address": "11111111111111111111111111111111",
                "chain_id": "solana",
                "decimals": 9
              }
            ]
          },
          "price": 196.45239612519998,
          "quantity": {
            "decimals": 9,
            "float": 0.000005,
            "int": "5000",
            "numeric": "0.000005000"
          },
          "value": 0.000982261980626
        },
        "transfers": [
          {
            "direction": "in",
            "fungible_info": {
              "name": "Tether USD",
              "symbol": "USDT",
              "flags": { "verified": true },
              "implementations": [
                { "address": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB", "chain_id": "solana", "decimals": 6 },
                { "address": "0xdac17f958d2ee523a2206206994597c13d831ec7", "chain_id": "ethereum", "decimals": 6 }
                /* + more chains */
              ]
            },
            "price": 1.0005395552,
            "quantity": { "decimals": 6, "float": 0.980106, "int": "980106", "numeric": "0.980106" },
            "sender": "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4",
            "recipient": "8BH9pjtgyZDC4iAQH5ZiYDZ1MDWC98xki2V8NzqqKW3K",
            "value": 0.9806348212888513
          },
          {
            "direction": "out",
            "fungible_info": {
              "name": "Solana",
              "symbol": "SOL",
              "flags": { "verified": true },
              "implementations": [
                {
                  "address": "11111111111111111111111111111111",
                  "chain_id": "solana",
                  "decimals": 9
                }
              ]
            },
            "price": 196.45239612519998,
            "quantity": { "decimals": 9, "float": 0.005, "int": "5000000", "numeric": "0.005000000" },
            "sender": "8BH9pjtgyZDC4iAQH5ZiYDZ1MDWC98xki2V8NzqqKW3K",
            "recipient": "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4",
            "value": 0.9822619806259999
          }
        ],
        "fee_token": "... (same fungible_info as fee)",
        "flags": { "is_trash": false }
      },
      "relationships": {
        "chain": { "id": "solana", "type": "chains" },
        "dapp": { "id": "jupiter", "type": "dapps" }
      }
    }
  ]
}
```

**Operational details:**[^4]

- Zerion retries delivery up to **3 times** for each event on failure.
- Delivery order is **not guaranteed**; do not assume webhook order equals on‑chain order.
- For full price/value enrichment (if missing), call the transactions endpoint by hash after receiving the webhook.[^16]
- With dev keys, Solana subscriptions are limited (e.g., 1 subscription, 5 wallets, 1‑week validity) and callback hosts must be approved for production.[^4]


### 5.3 Managing subscriptions

While the blog focuses on creation, it also notes management operations for subscriptions:[^4]

- List all subscriptions or fetch by ID
- Enable/disable (pause without deleting)
- Update `callback_url`
- Replace or patch `addresses`
- Change `chain_ids` (e.g. extend from Solana only to Solana + EVM)

These map to typical REST verbs on `/v1/tx-subscriptions` (GET, PATCH, DELETE); the exact payloads are documented in the API reference.

***

## 6. Chains \& Metadata

Zerion maintains an internal registry of supported chains and their IDs.[^17][^10]

### 6.1 List supported blockchains

**Endpoint (docs reference):**

```http
GET /v1/chains
```

or a similar path referenced as `listchains` in docs.[^17]

**Response:** A list of chains, each with:

- `id`: chain ID used across the API (e.g. `ethereum`, `base`, `solana`, `polygon`, `optimism`, `arbitrum`, etc.)[^3][^17][^13][^4]
- Explorer URLs
- Basic properties (name, layer, logo)

This list is useful to:

- Build chain pickers in UI
- Validate `filter[chain_ids]` and `chain_ids` for webhooks


### 6.2 Fungible \& NFT metadata

Fungible and NFT objects appear in `included` or nested in `fungible_info`/`nft_info` with fields such as:[^10][^12][^4]

- `name`, `symbol`
- `icon.url`
- `flags.verified`
- `implementations`: list of `chain_id`, on‑chain contract `address`, and `decimals`
- For NFTs, collection‑level fields (name, slug, floor price, media URLs)[^8][^10]

***

## 7. Errors, Status Codes, and Rate Limits

The OpenAPI spec and wrappers show Zerion follows **standard REST semantics**:[^15][^23]

- `200 OK`: success with full data
- `201 Created`: for resources like subscriptions
- `202 Accepted`: wallet data (portfolio, positions, NFTs) is being prepared; client must retry later[^23]
- `400 Bad Request`: invalid parameters or filters
- `401 Unauthorized`: missing/invalid API key
- `404 Not Found`: unknown resource (wallet, subscription, chain ID, etc.)
- `429 Too Many Requests`: rate limit exceeded (respect `Retry-After` header if returned)
- `5xx`: server‑side error

Error responses typically include a JSON body with an `errors` array following JSON:API conventions (code, title, detail).

**Rate‑limit strategy:**

- Free/dev keys: capped daily quota and low RPS; meant for local development and MVPs.[^1][^10]
- Production keys: much higher RPS, no strict long‑term cap, and customizable for enterprise (up to ~2K RPS on request).[^1]
- Quotas and current usage are visible in the Zerion dashboard.[^1][^10]

***

## 8. Typical Integration Patterns \& Best Practices

### 8.1 Basic portfolio tracker / wallet UI

1. **Obtain an API key** from Zerion API’s signup page and configure Basic auth.[^25][^1]
2. For each user wallet address:
    - Call `GET /v1/wallets/{address}/portfolio` for summary and PnL.
    - Call `GET /v1/wallets/{address}/positions` (optionally with `filter[positions]=only_complex`) for DeFi breakdown.[^7]
    - Call `GET /v1/wallets/{address}/transactions` for history.[^13][^12]
    - Call `GET /v1/wallets/{address}/nft-portfolio` + `nft-positions` for NFTs.[^11][^9][^8]
3. Use `filter[chain_ids]` to restrict chains per view (e.g., “show only Base positions”).[^6][^12][^7]
4. Implement **pagination** via `links.next` and `page[after]`.[^12][^13]

### 8.2 Real‑time notifications (mobile wallet, SocialFi, agents)

- Create a `tx-subscriptions` entry for each wallet the user follows or owns.[^16]
- Handle incoming webhook POSTs:
    - Verify signature headers (as described in the docs).
    - Parse the `transactions` object in `included` and surface:
        - Operation type (`trade`, `transfer`, `execute`)[^12][^4]
        - Assets and value
        - Protocol (`application_metadata` / `dapp`)[^4]
- For **up‑to‑date prices** in webhooks where `price`/`value` are `null`, query the transactions endpoint by `hash`.[^16]


### 8.3 Cross‑chain analytics \& dashboards

- Use `GET /v1/wallets/{address}/transactions` with `filter[chain_ids]` to focus on L2s or a subset of chains.[^13][^12]
- Generate PnL and trend charts with `GET /v1/wallets/{address}/chart` and the portfolio endpoint.[^14][^15]
- For DeFi analytics (risk, collateralization, LP breakdown), rely on `positions` endpoint with `filter[positions]=only_complex` and chain/protocol filters.[^7]


### 8.4 Testnets and staging

- Use the `X-Env` header to access testnets and staging environments; the same endpoints and schemas apply, but data comes from test networks.[^19][^9][^8]
- Keep separate API keys for dev/staging vs production.

***

## 9. Summary of Key Methods

Below is a concise overview of the main developer‑relevant endpoints and what to expect.


| Area | Method \& Path | Description |
| :-- | :-- | :-- |
| Portfolio | `GET /v1/wallets/{address}/portfolio` | Wallet’s total portfolio, per‑chain breakdown, and PnL summary.[^2][^22] |
| Positions | `GET /v1/wallets/{address}/positions` | Fungible + DeFi positions; rich filtering and sorting; `only_complex` for DeFi‑only.[^23][^7] |
| NFT portfolio | `GET /v1/wallets/{address}/nft-portfolio` | NFT holdings overview and valuation.[^11][^10] |
| NFT positions | `GET /v1/wallets/{address}/nft-positions` | Individual NFT positions per collection/token; filters by chain and collection.[^8][^9][^23] |
| NFT collections | `GET /v1/wallets/{address}/nft-collections` | Aggregated NFT collections held by the wallet.[^8] |
| Transactions | `GET /v1/wallets/{address}/transactions` | Multi‑chain normalized tx history with decoded operations and transfers.[^12][^13] |
| Chart | `GET /v1/wallets/{address}/chart` | Historical portfolio balance chart data.[^14][^15] |
| Webhooks | `POST /v1/tx-subscriptions` | Create a subscription to tx webhooks for specified addresses.[^4][^16] |
| Webhooks mgmt | `GET/PATCH/DELETE /v1/tx-subscriptions/{id}` | List, update, or delete subscriptions (enable, disable, patch addresses, etc.).[^4] |
| Chains | `GET /v1/chains` | List of supported chains and IDs used in filters and responses.[^17][^10] |


***

If you share the exact type of app (wallet, analytics, bot/agent, etc.) and stack (language/framework), a more concrete, end‑to‑end integration walkthrough with code samples tailored to that environment can be provided.
<span style="display:none">[^26][^27][^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^41][^42]</span>

<div align="center">⁂</div>

[^1]: https://zerion.io/api

[^2]: https://docs.zero.network/other-docs/zerion-api

[^3]: https://zerion.io/blog/top-10-crypto-wallet-data-apis-2025-guide/

[^4]: https://zerion.io/blog/solana-webhooks-zerion-api-real-time-transaction-alerts/

[^5]: https://zerion.io/blog/how-kirha-leverages-zerion-api-to-revolutionize-crypto-data-access/

[^6]: https://zerion.io/api/base

[^7]: https://zerion.io/blog/how-to-fetch-multichain-defi-positions-for-wallet-with-zerion-api/

[^8]: https://developers.zerion.io/reference/listwalletnftcollections

[^9]: https://developers.zerion.io/reference/listwalletnftpositions

[^10]: https://zerion.io/nft-api

[^11]: https://developers.zerion.io/reference/getwalletnftportfolio

[^12]: https://zerion.io/blog/how-to-track-layer-2-transactions/

[^13]: https://zerion.io/blog/how-to-track-cross-chain-transaction-history/

[^14]: https://developers.zerion.io/reference/getwalletchart

[^15]: https://raw.githubusercontent.com/smart-mcp-proxy/zerion-mcp-server/main/zerion_mcp_server/openapi_zerion.yaml

[^16]: https://zerion.io/blog/how-to-create-real-time-ethereum-transaction-notifications-with-zerion-api/

[^17]: https://developers.zerion.io/reference/supported-blockchains

[^18]: https://developers.zerion.io/reference/authentication

[^19]: https://developers.zerion.io/reference/listwallettransactions

[^20]: https://github.com/zeriontech/api-docs/blob/master/featured-partners.md

[^21]: https://developers.zerion.io/reference/wallets

[^22]: https://developers.zerion.io/reference/getwalletportfolio

[^23]: https://github.com/darrylyeo/blockhead/blob/main/src/api/zerion/api/index.ts

[^24]: https://zerion.io/defi-portfolio-tracker

[^25]: https://help.zerion.io/en/articles/11320781-getting-started-with-the-zerion-api-docs-access-and-keys

[^26]: https://developers.zerion.io/reference/intro/getting-started

[^27]: https://developers.zerion.io/reference/endpoints-and-schema-details

[^28]: https://www.alchemy.com/case-studies/zerion

[^29]: https://zerion.io/api/monad

[^30]: https://zerion.io/api-clients-wallets-defi

[^31]: https://github.com/zeriontech/api-docs

[^32]: https://www.meshpay.com/blog/does-zerion-wallet-have-an-api

[^33]: https://developers.zerion.io/reference/feedback

[^34]: https://zerion.io/blog/guide-to-building-on-monad-with-zerion-api/

[^35]: https://www.youtube.com/watch?v=hg6HX_4CP_A

[^36]: https://developers.zerion.io/reference/featured-partners

[^37]: https://earn.superteam.fun/listing/build-a-consumer-app-on-solana-using-the-zerion-api

[^38]: https://www.youtube.com/watch?v=tT7InlZnRmM

[^39]: https://www.coingecko.com/learn/zerion-case-study

[^40]: https://dlthub.com/workspace/source/zerion

[^41]: https://zerion.my.site.com/helpcenter/s/article/VIDEOBuildingyourownZerionDocument66b5d5b9dae8e

[^42]: https://core.app/discover/project/zerion-wallet

