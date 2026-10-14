from unittest.mock import AsyncMock

import pytest

from shop.services import AsyncStockService


@pytest.mark.asyncio
async def test_available_quantity():
    provider = AsyncMock()
    provider.fetch_stock.return_value = {"quantity": "7"}
    service = AsyncStockService(provider)

    result = await service.available_quantity(1)

    assert result == 7
    provider.fetch_stock.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_provider_failure_propagates():
    provider = AsyncMock()
    provider.fetch_stock.side_effect = ConnectionError("Network error")
    service = AsyncStockService(provider)

    with pytest.raises(ConnectionError, match="Network"):
        await service.available_quantity(1)

    provider.fetch_stock.assert_awaited_once()


@pytest.mark.asyncio
async def test_malformed_provider_response():
    provider = AsyncMock()
    provider.fetch_stock.return_value = {"qty": 1}

    with pytest.raises(KeyError):
        await AsyncStockService(provider).available_quantity(1)
