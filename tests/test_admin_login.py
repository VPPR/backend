from app.server.routes.admin import admin_login
from app.server.auth.admin import validate_login
from fastapi.testclient import TestClient
from app.server.routes.admin import router as admin_router

client = TestClient(admin_router)

def test_admin_login():
    response = client.post("/login",json={"username":"test1@yahoomail.com", 
    "password":"KillCOVID"}, headers = {"accept":"application/json", "Content-type":"application/json"})
    assert response.status_code == 200

def test_admin_signup():
    response = client.post("/",json={"fullname":"test","email":"test5@yahoomail.com",
    "password":"KillCOVID"}, headers = {"accept":"application/json", "Content-type":"application/json"})
    assert response.status_code == 200