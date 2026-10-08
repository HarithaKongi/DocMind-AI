from functools import lru_cache
from urllib.parse import urlparse

import httpx
from supabase import Client, create_client

from app.core.config import settings


def _clean(value: str) -> str:
    return value.strip().strip('"').strip("'").strip()


def _create_client() -> Client:
    url = _clean(settings.supabase_url)
    key = _clean(settings.supabase_key)

    if not url or not key:
        raise RuntimeError(
            "Supabase is not configured. Set SUPABASE_URL and SUPABASE_KEY."
        )

    return create_client(url, key)


@lru_cache
def get_supabase_client() -> Client:
    return _create_client()


def get_user_supabase_client(access_token: str) -> Client:
    client = _create_client()
    client.postgrest.auth(access_token.strip())
    return client


async def diagnose_supabase() -> dict[str, object]:
    url = _clean(settings.supabase_url)
    key = _clean(settings.supabase_key)

    if not url or not key:
        return {
            "configured": False,
            "reason": "SUPABASE_URL or SUPABASE_KEY is empty",
        }

    if key.startswith("sb_publishable_"):
        key_type = "publishable"
    elif key.startswith("sb_secret_"):
        key_type = "secret"
    elif key.startswith("eyJ"):
        key_type = "legacy-jwt"
    else:
        key_type = "unknown"

    host = urlparse(url).netloc or "invalid-host"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{url.rstrip('/')}/auth/v1/settings",
                headers={"apikey": key},
            )

        return {
            "configured": True,
            "key_type": key_type,
            "host": host,
            "auth_settings_status": response.status_code,
            "auth_settings_ok": response.is_success,
            "message": (
                "Supabase API key accepted."
                if response.is_success
                else response.text[:300]
            ),
        }
    except httpx.HTTPError as exc:
        return {
            "configured": True,
            "key_type": key_type,
            "host": host,
            "auth_settings_status": None,
            "auth_settings_ok": False,
            "message": f"Supabase connection failed: {exc}",
        }
