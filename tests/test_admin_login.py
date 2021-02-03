from app.server.routes.admin import admin_login
from app.server.auth.admin import validate_login
from fastapi.testclient import TestClient
from app.server.routes.admin import router as admin_router

client = TestClient(admin_router)

def test_admin_login():
    response = client.post("/login",json={"username":"vigneshiyer666666@gmail.com", 
    "password":"India@70"}, headers = {"accept":"application/json", "Content-type":"application/json"})
    assert response.status_code == 200