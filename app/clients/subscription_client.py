from typing import Optional
import httpx
from fastapi import HTTPException
from ..config import settings

async def get_user_subscription_status_from_subscriptions(
    user_id: int,
    authorization_header: str,
) -> Optional[dict]:
    """
    Llama a GET /api/v1/subscriptions?user_id={user_id} en el subscriptions-service
    y devuelve la primera (o None).
    """
    url = f"{settings.SUBSCRIPTIONS_BASE_URL}/api/v1/subscriptions"
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(
            url,
            params={"user_id": user_id},
            headers={"Authorization": authorization_header},
        )

    if resp.status_code == 404:
        return None
    if resp.status_code not in (200, 201):
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Subscriptions service error: {resp.text}",
        )

    subs = resp.json()
    if not subs:
        return None

    # asumimos que la última es la más reciente
    return subs[-1]
