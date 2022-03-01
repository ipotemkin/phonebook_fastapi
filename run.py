from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from uvicorn import run

from app.errors import (
    NotFoundError,
    NoContentError,
    ValidationError,
    DatabaseError,
    BadRequestError,
)
from app import views

tags_metadata = [
    {
        "name": "phones",
        "description": "Операции с телефонами",
    },
]

app = FastAPI(
    title="Simple phonebook on FastAPI",
    version="1.0.0",
    contact={
        "name": "Igor Potemkin",
        "email": "ipotemkin@rambler.ru",
    },
    openapi_tags=tags_metadata,
    docs_url="/",
)

app.include_router(views.router)


@app.on_event("startup")
async def on_startup():
    pass


@app.on_event("shutdown")
async def on_shutdown():
    pass


# exception handlers
@app.exception_handler(404)
@app.exception_handler(NotFoundError)
def not_found_error(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"message": "Not Found"})


@app.exception_handler(NoContentError)
def no_content_error(request: Request, exc: NoContentError):
    return JSONResponse(status_code=204, content={"message": "No Content"})


@app.exception_handler(DatabaseError)
def database_error(request: Request, exc: DatabaseError):
    return JSONResponse(status_code=400, content={"message": "Database Error"})


@app.exception_handler(BadRequestError)
def bad_request_error(request: Request, exc: BadRequestError):
    return JSONResponse(status_code=400, content={"message": "Bad Request"})


@app.exception_handler(ValidationError)
def validation_error(request: Request, exc: ValidationError):
    return JSONResponse(status_code=400, content={"message": "Validation Error"})


if __name__ == "__main__":
    run("run:app", host="localhost", port=5000, reload=True)
