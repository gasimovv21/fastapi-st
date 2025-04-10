import uvicorn


from fastapi import FastAPI
from routers.items import router as items_router


app = FastAPI(
    title="FastAPI Shop",
    description="Basic FastAPI inventory with filtering and CRUD",
    version="1.0.0"
)

app.include_router(items_router)


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
