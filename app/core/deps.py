from fastapi import Header, HTTPException, status

from app.core.config import settings


def require_admin_key(x_admin_key: str | None = Header(default=None)) -> None:
    """
    Simple guard:
    - If ADMIN_API_KEY is set in .env, then requests MUST include X-Admin-Key header.
    - If ADMIN_API_KEY is not set, we block access (fail closed).
    """

    if not settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin access not configured",
        )

    if x_admin_key != settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin key",
        )
