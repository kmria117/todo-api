from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.exceptions import (
    InvalidTaskError,
    TaskAlreadyDoneError,
    TaskNotFoundError,
)

app = FastAPI(title="Todo API")
app.include_router(router)


def _handler(code: int):
    async def handle(_: Request, exc: Exception):
        return JSONResponse(status_code=code, content={"detail": str(exc)})
    return handle


app.add_exception_handler(TaskNotFoundError, _handler(404))
app.add_exception_handler(InvalidTaskError, _handler(400))
app.add_exception_handler(TaskAlreadyDoneError, _handler(409))
