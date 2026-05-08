"""
License activation and heartbeat loop.
This module is compiled to .so by Cython.
"""

import asyncio
import contextlib
import logging

import httpx

from core.config import settings

logger = logging.getLogger(__name__)

HEARTBEAT_INTERVAL = 600  # 10 minutes
GRACE_PERIOD_SECONDS = 7 * 24 * 3600  # 7 days


class LicenseManager:
    def __init__(self) -> None:
        self._lease_token: str | None = None
        self._heartbeat_task: asyncio.Task | None = None

    async def activate(self) -> None:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{settings.license.license_server_url}/v1/license/activate",
                json={
                    "license_key": settings.license.license_key,
                    "deployment_id": settings.license.deployment_id,
                },
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            self._lease_token = data["lease_token"]
            logger.info("License activated, lease_token acquired")

    async def _heartbeat(self) -> None:
        while True:
            await asyncio.sleep(HEARTBEAT_INTERVAL)
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        f"{settings.license.license_server_url}/v1/license/heartbeat",
                        json={
                            "license_key": settings.license.license_key,
                            "deployment_id": settings.license.deployment_id,
                            "lease_token": self._lease_token,
                        },
                        timeout=15,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    self._lease_token = data.get("lease_token", self._lease_token)
                    logger.debug("Heartbeat OK")
            except Exception as exc:
                logger.warning("Heartbeat failed: %s", exc)

    def start_heartbeat(self) -> None:
        self._heartbeat_task = asyncio.create_task(self._heartbeat())

    async def stop(self) -> None:
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._heartbeat_task


license_manager = LicenseManager()
