import uvicorn


from fastapi import FastAPI
from routers import items


app = FastAPI()

app.include_router(items.router)


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
