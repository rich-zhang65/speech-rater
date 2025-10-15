from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import settings
import httpx


security = HTTPBearer()


class Auth0Verifier:
    """Verify Auth0 JWT tokens."""
    
    def __init__(self):
        self.domain = settings.AUTH0_DOMAIN
        self.api_audience = settings.AUTH0_API_AUDIENCE
        self.issuer = settings.AUTH0_ISSUER
        self.algorithms = [settings.AUTH0_ALGORITHMS]
    
    async def get_jwks(self):
        """Fetch JSON Web Key Set from Auth0."""
        url = f"https://{self.domain}/.well-known/jwks.json"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()
    
    async def verify_token(self, token: str) -> dict:
        """
        Verify and decode JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload
        """
        try:
            # In production, you would fetch and cache the JWKS
            # For MVP, we'll do basic validation
            unverified_header = jwt.get_unverified_header(token)
            
            # Decode and verify the token
            payload = jwt.decode(
                token,
                key="",  # In production, use proper JWKS verification
                algorithms=self.algorithms,
                audience=self.api_audience,
                issuer=self.issuer,
                options={"verify_signature": False}  # For MVP only - MUST enable in production
            )
            
            return payload
        
        except JWTError as e:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid authentication credentials: {str(e)}"
            )


auth_verifier = Auth0Verifier()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    Dependency to get current authenticated user.
    Use this in routes that require authentication.
    
    Example:
        @router.get("/protected")
        async def protected_route(user: dict = Depends(get_current_user)):
            return {"user_id": user["sub"]}
    """
    token = credentials.credentials
    return await auth_verifier.verify_token(token)


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Security(security, auto_error=False)
) -> dict | None:
    """
    Dependency to optionally get authenticated user.
    Returns None if no valid token is provided.
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        return await auth_verifier.verify_token(token)
    except HTTPException:
        return None

