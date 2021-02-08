from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .auth.jwt_bearer import JWTBearer
from .routes.user import router as UserRouter

app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

token_listener = JWTBearer()

@app.get('/',tags=['Root'])
async def read_root():
    return {'message':'Reliability issues = bugres'}

# app.include_router(AdminRouter, tags=['Administrator'],prefix='/admin')
# app.include_router(UserRouter, tags=['Users'],prefix='/user',dependencies=[Depends(token_listener)])

app.include_router(
    UserRouter,
    tags=[
        'User'
    ],
    prefix='/user'
)
