from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.base import AppException

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_excption_handler(
        request : Request,
        exc: AppException,
    ):

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success":False,
                "message": exc.detail,
                "error_code": exc.error_code,
            },
        )