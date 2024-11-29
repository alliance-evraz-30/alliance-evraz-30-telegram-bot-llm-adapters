import asyncio

import uvicorn
from fastapi import FastAPI

from src import config
from src.adapters.routers.context_router import context_router
from src.adapters.routers.project_router import project_router
from src.bootstrap import get_container

app = FastAPI()

app.include_router(project_router)
app.include_router(context_router)


def main():
    startup_service = get_container().startup_service()
    asyncio.run(startup_service.execute())
    uvicorn.run(app, host=config.HOST, port=config.PORT)


if __name__ == "__main__":
    main()

