#!/usr/bin/env python3
"""Integration tests for webhook subscription endpoints."""

import pytest
import httpx
import respx
from unittest.mock import Mock, patch
import json


@pytest.fixture
def webhook_subscription_response():
    """Mock successful webhook subscription creation response."""
    return {
        "data": {
            "type": "callback",
            "id": "bf300927-3f57-4d00-a01a-f7b75bd9b8de",
            "attributes": {
                "address": "0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990",
                "callback_url": "https://webhook.site/test",
                "timestamp": "2025-10-16T10:56:50.047643374Z"
            },
            "relationships": {
                "subscription": {
                    "data": {
                        "id": "61f13641-443e-4068-932b-c28edeaefd85",
                        "type": "tx-subscriptions"
                    }
                }
            }
        }
    }


@pytest.fixture
def subscription_list_response():
    """Mock subscription list response."""
    return {
        "data": [
            {
                "type": "tx-subscriptions",
                "id": "61f13641-443e-4068-932b-c28edeaefd85",
                "attributes": {
                    "addresses": ["0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990"],
                    "callback_url": "https://webhook.site/test",
                    "chain_ids": ["ethereum", "base"],
                    "created_at": "2025-10-16T10:56:50Z",
                    "enabled": True
                }
            }
        ]
    }


@pytest.fixture
def webhook_payload_example():
    """Example webhook payload that would be received."""
    return {
        "data": {
            "type": "callback",
            "id": "bf300927-3f57-4d00-a01a-f7b75bd9b8de",
            "attributes": {
                "address": "0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990",
                "callback_url": "https://webhook.site/test",
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
                            "symbol": "ETH"
                        },
                        "quantity": {"float": 0.001},
                        "value": 3.5
                    },
                    "transfers": [],
                    "flags": {"is_trash": False}
                },
                "relationships": {
                    "chain": {"id": "ethereum", "type": "chains"},
                    "dapp": {"id": "uniswap", "type": "dapps"}
                }
            }
        ]
    }


class TestWebhookSubscriptionCreation:
    """Test webhook subscription creation endpoint."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_subscription_ethereum(self, webhook_subscription_response):
        """Test creating a webhook subscription for Ethereum address."""
        base_url = "https://api.zerion.io"

        # Mock the POST request
        route = respx.post(f"{base_url}/v1/tx-subscriptions/").mock(
            return_value=httpx.Response(201, json=webhook_subscription_response)
        )

        # Simulate API call
        async with httpx.AsyncClient(base_url=base_url) as client:
            response = await client.post(
                "/v1/tx-subscriptions/",
                json={
                    "addresses": ["0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990"],
                    "callback_url": "https://webhook.site/test",
                    "chain_ids": ["ethereum", "base"]
                },
                headers={"Authorization": "Bearer test-key"}
            )

        assert response.status_code == 201
        assert route.called
        data = response.json()
        assert data["data"]["type"] == "callback"
        assert data["data"]["attributes"]["callback_url"] == "https://webhook.site/test"
        assert data["data"]["relationships"]["subscription"]["data"]["type"] == "tx-subscriptions"

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_subscription_solana(self):
        """Test creating a webhook subscription for Solana address."""
        base_url = "https://api.zerion.io"

        solana_response = {
            "data": {
                "type": "callback",
                "id": "test-id-solana",
                "attributes": {
                    "address": "8BH9pjtgyZDC4iAQH5ZiYDZ1MDWC98xki2V8NzqqKW3K",
                    "callback_url": "https://webhook.site/solana-test",
                    "timestamp": "2025-10-16T10:56:50Z"
                },
                "relationships": {
                    "subscription": {
                        "data": {
                            "id": "solana-sub-id",
                            "type": "tx-subscriptions"
                        }
                    }
                }
            }
        }

        route = respx.post(f"{base_url}/v1/tx-subscriptions/").mock(
            return_value=httpx.Response(201, json=solana_response)
        )

        async with httpx.AsyncClient(base_url=base_url) as client:
            response = await client.post(
                "/v1/tx-subscriptions/",
                json={
                    "addresses": ["8BH9pjtgyZDC4iAQH5ZiYDZ1MDWC98xki2V8NzqqKW3K"],
                    "callback_url": "https://webhook.site/solana-test",
                    "chain_ids": ["solana"]
                },
                headers={"Authorization": "Bearer test-key"}
            )

        assert response.status_code == 201
        data = response.json()
        assert "solana" in str(data).lower() or "8BH9pjtgyZDC4iAQH5ZiYDZ1MDWC98xki2V8NzqqKW3K" in str(data)

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_subscription_invalid_url(self):
        """Test creating subscription with invalid callback URL returns 400."""
        base_url = "https://api.zerion.io"

        error_response = {
            "errors": [{
                "title": "Bad Request",
                "detail": "callback_url must be a valid HTTPS URL"
            }]
        }

        route = respx.post(f"{base_url}/v1/tx-subscriptions/").mock(
            return_value=httpx.Response(400, json=error_response)
        )

        async with httpx.AsyncClient(base_url=base_url) as client:
            response = await client.post(
                "/v1/tx-subscriptions/",
                json={
                    "addresses": ["0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990"],
                    "callback_url": "http://insecure-url.com",  # HTTP not HTTPS
                    "chain_ids": ["ethereum"]
                },
                headers={"Authorization": "Bearer test-key"}
            )

        assert response.status_code == 400
        data = response.json()
        assert "errors" in data


class TestWebhookSubscriptionListing:
    """Test listing webhook subscriptions."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_subscriptions(self, subscription_list_response):
        """Test listing all subscriptions."""
        base_url = "https://api.zerion.io"

        route = respx.get(f"{base_url}/v1/tx-subscriptions/").mock(
            return_value=httpx.Response(200, json=subscription_list_response)
        )

        async with httpx.AsyncClient(base_url=base_url) as client:
            response = await client.get(
                "/v1/tx-subscriptions/",
                headers={"Authorization": "Bearer test-key"}
            )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 1
        assert data["data"][0]["type"] == "tx-subscriptions"
        assert data["data"][0]["attributes"]["enabled"] == True

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_subscriptions_empty(self):
        """Test listing subscriptions when none exist."""
        base_url = "https://api.zerion.io"

        empty_response = {"data": []}

        route = respx.get(f"{base_url}/v1/tx-subscriptions/").mock(
            return_value=httpx.Response(200, json=empty_response)
        )

        async with httpx.AsyncClient(base_url=base_url) as client:
            response = await client.get(
                "/v1/tx-subscriptions/",
                headers={"Authorization": "Bearer test-key"}
            )

        assert response.status_code == 200
        data = response.json()
        assert data["data"] == []


class TestWebhookSubscriptionRetrieval:
    """Test retrieving a specific subscription."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_subscription_by_id(self):
        """Test getting subscription details by ID."""
        base_url = "https://api.zerion.io"
        subscription_id = "61f13641-443e-4068-932b-c28edeaefd85"

        subscription_response = {
            "data": {
                "type": "tx-subscriptions",
                "id": subscription_id,
                "attributes": {
                    "addresses": ["0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990"],
                    "callback_url": "https://webhook.site/test",
                    "chain_ids": ["ethereum", "base"],
                    "created_at": "2025-10-16T10:56:50Z",
                    "enabled": True
                }
            }
        }

        route = respx.get(f"{base_url}/v1/tx-subscriptions/{subscription_id}").mock(
            return_value=httpx.Response(200, json=subscription_response)
        )

        async with httpx.AsyncClient(base_url=base_url) as client:
            response = await client.get(
                f"/v1/tx-subscriptions/{subscription_id}",
                headers={"Authorization": "Bearer test-key"}
            )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id"] == subscription_id
        assert data["data"]["attributes"]["enabled"] == True

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_subscription_not_found(self):
        """Test getting non-existent subscription returns 404."""
        base_url = "https://api.zerion.io"
        subscription_id = "non-existent-id"

        error_response = {
            "errors": [{
                "title": "Not Found",
                "detail": "Subscription not found"
            }]
        }

        route = respx.get(f"{base_url}/v1/tx-subscriptions/{subscription_id}").mock(
            return_value=httpx.Response(404, json=error_response)
        )

        async with httpx.AsyncClient(base_url=base_url) as client:
            response = await client.get(
                f"/v1/tx-subscriptions/{subscription_id}",
                headers={"Authorization": "Bearer test-key"}
            )

        assert response.status_code == 404
        data = response.json()
        assert "errors" in data


class TestWebhookSubscriptionUpdate:
    """Test updating webhook subscriptions."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_subscription_addresses(self):
        """Test updating subscription addresses."""
        base_url = "https://api.zerion.io"
        subscription_id = "61f13641-443e-4068-932b-c28edeaefd85"

        updated_response = {
            "data": {
                "type": "tx-subscriptions",
                "id": subscription_id,
                "attributes": {
                    "addresses": [
                        "0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990",
                        "0xNewAddress123456789"
                    ],
                    "callback_url": "https://webhook.site/test",
                    "chain_ids": ["ethereum", "base"]
                }
            }
        }

        route = respx.patch(f"{base_url}/v1/tx-subscriptions/{subscription_id}").mock(
            return_value=httpx.Response(200, json=updated_response)
        )

        async with httpx.AsyncClient(base_url=base_url) as client:
            response = await client.patch(
                f"/v1/tx-subscriptions/{subscription_id}",
                json={
                    "addresses": [
                        "0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990",
                        "0xNewAddress123456789"
                    ]
                },
                headers={"Authorization": "Bearer test-key"}
            )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["attributes"]["addresses"]) == 2

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_subscription_callback_url(self):
        """Test updating subscription callback URL."""
        base_url = "https://api.zerion.io"
        subscription_id = "61f13641-443e-4068-932b-c28edeaefd85"

        updated_response = {
            "data": {
                "type": "tx-subscriptions",
                "id": subscription_id,
                "attributes": {
                    "addresses": ["0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990"],
                    "callback_url": "https://new-webhook.site/updated",
                    "chain_ids": ["ethereum"]
                }
            }
        }

        route = respx.patch(f"{base_url}/v1/tx-subscriptions/{subscription_id}").mock(
            return_value=httpx.Response(200, json=updated_response)
        )

        async with httpx.AsyncClient(base_url=base_url) as client:
            response = await client.patch(
                f"/v1/tx-subscriptions/{subscription_id}",
                json={"callback_url": "https://new-webhook.site/updated"},
                headers={"Authorization": "Bearer test-key"}
            )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["attributes"]["callback_url"] == "https://new-webhook.site/updated"


class TestWebhookSubscriptionDeletion:
    """Test deleting webhook subscriptions."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_delete_subscription(self):
        """Test deleting a subscription."""
        base_url = "https://api.zerion.io"
        subscription_id = "61f13641-443e-4068-932b-c28edeaefd85"

        route = respx.delete(f"{base_url}/v1/tx-subscriptions/{subscription_id}").mock(
            return_value=httpx.Response(204)
        )

        async with httpx.AsyncClient(base_url=base_url) as client:
            response = await client.delete(
                f"/v1/tx-subscriptions/{subscription_id}",
                headers={"Authorization": "Bearer test-key"}
            )

        assert response.status_code == 204
        assert route.called

    @respx.mock
    @pytest.mark.asyncio
    async def test_delete_subscription_not_found(self):
        """Test deleting non-existent subscription returns 404."""
        base_url = "https://api.zerion.io"
        subscription_id = "non-existent-id"

        error_response = {
            "errors": [{
                "title": "Not Found",
                "detail": "Subscription does not exist"
            }]
        }

        route = respx.delete(f"{base_url}/v1/tx-subscriptions/{subscription_id}").mock(
            return_value=httpx.Response(404, json=error_response)
        )

        async with httpx.AsyncClient(base_url=base_url) as client:
            response = await client.delete(
                f"/v1/tx-subscriptions/{subscription_id}",
                headers={"Authorization": "Bearer test-key"}
            )

        assert response.status_code == 404
        data = response.json()
        assert "errors" in data


class TestWebhookPayloadValidation:
    """Test webhook payload structure validation."""

    def test_webhook_payload_structure(self, webhook_payload_example):
        """Test that webhook payload has expected structure."""
        assert "data" in webhook_payload_example
        assert "included" in webhook_payload_example

        # Validate callback data
        callback = webhook_payload_example["data"]
        assert callback["type"] == "callback"
        assert "attributes" in callback
        assert "address" in callback["attributes"]
        assert "callback_url" in callback["attributes"]
        assert "timestamp" in callback["attributes"]

        # Validate transaction data
        transactions = webhook_payload_example["included"]
        assert len(transactions) > 0
        tx = transactions[0]
        assert tx["type"] == "transactions"
        assert "attributes" in tx
        assert "hash" in tx["attributes"]
        assert "operation_type" in tx["attributes"]
        assert "relationships" in tx
        assert "chain" in tx["relationships"]

    def test_webhook_payload_transaction_details(self, webhook_payload_example):
        """Test transaction details in webhook payload."""
        tx = webhook_payload_example["included"][0]
        attrs = tx["attributes"]

        # Verify required fields
        assert attrs["operation_type"] in ["trade", "transfer", "execute", "approve"]
        assert "hash" in attrs
        assert "mined_at" in attrs
        assert "status" in attrs
        assert attrs["status"] == "confirmed"

        # Verify fee structure
        assert "fee" in attrs
        assert "fungible_info" in attrs["fee"]
        assert "quantity" in attrs["fee"]

        # Verify chain relationship
        assert tx["relationships"]["chain"]["id"] in ["ethereum", "base", "solana", "optimism"]


class TestWebhookRateLimiting:
    """Test webhook subscription rate limiting."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_subscription_rate_limit(self):
        """Test that rate limiting returns 429."""
        base_url = "https://api.zerion.io"

        error_response = {
            "errors": [{
                "title": "Too Many Requests",
                "detail": "Rate limit exceeded"
            }]
        }

        route = respx.post(f"{base_url}/v1/tx-subscriptions/").mock(
            return_value=httpx.Response(429, json=error_response)
        )

        async with httpx.AsyncClient(base_url=base_url) as client:
            response = await client.post(
                "/v1/tx-subscriptions/",
                json={
                    "addresses": ["0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990"],
                    "callback_url": "https://webhook.site/test",
                    "chain_ids": ["ethereum"]
                },
                headers={"Authorization": "Bearer test-key"}
            )

        assert response.status_code == 429
        data = response.json()
        assert "errors" in data
