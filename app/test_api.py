from fastapi.testclient import TestClient


from app.main import app

# like python requests
client = TestClient(app)

def test_get_home():
    response = client.get("/") # i.e requests.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']
