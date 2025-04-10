import uvicorn


from fastapi import FastAPI
from routers.items import router as items_router


app = FastAPI()

app.include_router(items_router)


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
