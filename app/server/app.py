from fastapi import FastAPI, Depends

from .auth.jwt_bearer import JWTBearer
from .routes.user import router as UserRouter
from .routes.admin import router as AdminRouter

app = FastAPI()

token_listener = JWTBearer()

@app.get("/",tags=["Root"])
async def read_root():
    return {"message":"Reliability issues = bugres"}

app.include_router(AdminRouter, tags=["Administrator"],prefix="/admin")
app.include_router(UserRouter, tags=["Users"],prefix="/user",dependencies=[Depends(token_listener)])