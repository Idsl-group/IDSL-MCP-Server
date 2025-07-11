import jwt
from fastapi import HTTPException

SECRET = "your_secret"

def check_scope(tool_name: str, token: str) -> bool:
    print(f"check_scope called for tool '{tool_name}'")
    print(f"Raw token: {token}")

    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        print("Decoded payload:", payload)

        scopes = payload.get("scopes", []) 
        print(f"Allowed scopes from token: {scopes}")

        authorized = ("tools:" + tool_name) in scopes
        print(f"Is tool '{tool_name}' authorized? {authorized}")
        return authorized

    except jwt.PyJWTError as e:
        print("Token decode failed:", str(e))
        raise HTTPException(status_code=403, detail="Invalid token")
