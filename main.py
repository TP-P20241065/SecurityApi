import uvicorn
from fastapi import FastAPI

from config.connection import prisma_connection
from report_management.controller import report_controller
from shared.exception.http_error_handler import HTTPErrorHandler
from unit_management.controller import driver_controller, unit_controller, camera_controller


def init_app():
    app = FastAPI(
        title="Security System",
        description="FastAPI Prisma",
        version="1.0.0",
    )
    app.add_middleware(HTTPErrorHandler)

    # app.include_router(prefix="/drivers", tags=["Drivers"], router=driver_router)

    @app.on_event("startup")
    async def startup():
        print("Start Server")
        await prisma_connection.connect()

    @app.on_event("shutdown")
    async def shutdown():
        print("Stop Server")
        await prisma_connection.disconnect()

    @app.get("/")
    def home():
        return {"Welcome Home!"}

    app.include_router(driver_controller.router)
    app.include_router(unit_controller.router)
    app.include_router(camera_controller.router)
    app.include_router(report_controller.router)

    return app


app = init_app()

# Registrar los routers


# Punto de entrada principal
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
