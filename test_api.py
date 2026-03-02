import urllib.request
import urllib.parse
import json

# Test health endpoint
try:
    response = urllib.request.urlopen('http://localhost:8000/health')
    data = response.read().decode()
    print(f"Health check: {data}")
except Exception as e:
    print(f"Health check failed: {e}")

# Test chat endpoint
try:
    data = json.dumps({"user_id": "test", "message": "Hello"}).encode('utf-8')
    req = urllib.request.Request(
        'http://localhost:8000/chat',
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    response = urllib.request.urlopen(req)
    result = response.read().decode()
    print(f"Chat response: {result}")
except Exception as e:
    print(f"Chat failed: {e}")
