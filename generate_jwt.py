import jwt

SECRET = "your_secret"
payload = {
    "sub": "test-user",
    "scopes": ["tools:add", "tools:subtract", "tools:divide"]
}

token = jwt.encode(payload, SECRET, algorithm="HS256")
print(token)
