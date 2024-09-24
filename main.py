import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from config.connection import prisma_connection
from report_management.controller import report_controller
from security.controller import auth_controller
from shared.exception.http_error_handler import HTTPErrorHandler
from unit_management.controller import driver_controller, unit_controller, camera_controller
from user_management.controller import user_controller


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start Server")
    await prisma_connection.connect()

    yield

    print("Stop Server")
    await prisma_connection.disconnect()


def init_app():
    app = FastAPI(
        title="Security System",
        description="FastAPI Prisma",
        version="1.0.0",
        lifespan=lifespan
    )

    # Configuración del CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(HTTPErrorHandler)

    @app.get("/")
    def home():
        file_path = os.path.join(os.getcwd(), 'shared', 'presentation', 'presentation.html')
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            return HTMLResponse(content=html_content)

    app.include_router(driver_controller.router)
    app.include_router(unit_controller.router)
    app.include_router(camera_controller.router)
    app.include_router(report_controller.router)
    app.include_router(user_controller.router)
    app.include_router(auth_controller.router)

    return app


app = init_app()

# Punto de entrada principal
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

