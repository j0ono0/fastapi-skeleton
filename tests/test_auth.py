from fastapi.testclient import TestClient
from server import main
from server.user.authentication import Token

#######################################

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database import db_config

engine = create_engine(
    "sqlite:///tests/test-data.db", connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_config.Base.metadata.create_all(bind=engine)

def get_test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#######################################

client = TestClient(main.app)

main.app.dependency_overrides[db_config.get_db] = get_test_db

def test_read_main():
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {
        'homepage': True,
        'fastapi': 'Working OK. Try user: pass below...',
        'admin@johnnewall.com': 'admin'
    }

def test_create_user():
    response = client.put(
        "/user/",
        json={
            "email": "admin@johnnewall.com",
            "password": "admin"
        }
    )
    assert response.status_code == 200
""" 
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
"""