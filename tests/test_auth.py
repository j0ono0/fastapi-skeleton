from fastapi.testclient import TestClient
from server.main import app
from server.authentication import Token

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        'homepage': True,
        'fastapi': 'Working OK. Try user: pass below...',
        'admin@johnnewall.com': 'admin'
    }

def test_user_authenticate():
    response = client.post(
        "/auth/token",
        data={
            "grant_type":"password", 
            "username":"admin@johnnewall.com", 
            "password":"admin"
        }
    )
    assert response.status_code == 200
    assert Token(**response.json())

    
        