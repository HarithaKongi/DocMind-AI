from functools import lru_cache

from supabase import Client, create_client

from app.core.config import settings


def _create_client() -> Client:
    if not settings.supabase_url or not settings.supabase_key:
        raise RuntimeError(
            "Supabase is not configured. Set SUPABASE_URL and SUPABASE_KEY."
        )

    return create_client(
        settings.supabase_url,
        settings.supabase_key,
    )


@lru_cache
def get_supabase_client() -> Client:
    return _create_client()


def get_user_supabase_client(access_token: str) -> Client:
    client = _create_client()
    client.postgrest.auth(access_token)
    return client
