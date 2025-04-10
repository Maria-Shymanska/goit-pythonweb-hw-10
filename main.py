from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api import utils, contacts, auth, users
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse


app = FastAPI()

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"error": "Request limit exceeded. Please try again later."},
    )


app.include_router(utils.router, prefix="/api/v1")
app.include_router(contacts.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
