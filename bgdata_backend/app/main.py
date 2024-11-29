from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import paper, service, user
from app.utils.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
  create_db_and_tables()
  yield

app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(paper.router)
app.include_router(service.router)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get('/')
async def root():
  return {'message': 'Hello from LinkedPapers!'}


if __name__ == '__main__':
  uvicorn.run(app, host='127.0.0.1', port=8000)
