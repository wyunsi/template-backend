from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    with (
        patch("core.license.manager.license_manager.activate", new_callable=AsyncMock),
        patch("core.license.manager.license_manager.start_heartbeat"),
        patch("core.license.manager.license_manager.stop", new_callable=AsyncMock),
    ):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            yield ac
