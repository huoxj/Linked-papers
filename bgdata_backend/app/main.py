import uvicorn
from fastapi import FastAPI

from app.routers import paper, service, user

app = FastAPI()

app.include_router(user.router)
app.include_router(paper.router)
app.include_router(service.router)


@app.get('/')
async def root():
  return {'message': 'Hello from LinkedPapers!'}


if __name__ == '__main__':
  uvicorn.run(app, host='127.0.0.1', port=8000)
