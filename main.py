from fastapi import FastAPI, HTTPException, Request
from limits import RateLimitItemPerMinute
from limits.storage.redis import RedisStorage

# Ініціалізація FastAPI
app = FastAPI()

# Налаштування підключення до Redis
# Використовує Redis за замовчуванням (локальний сервер на 6379 порту)
storage = RedisStorage("redis://localhost:6379")

# Ліміт: 5 запитів на хвилину
LIMIT = RateLimitItemPerMinute(5)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Використовуємо IP клієнта як ключ
    client_ip = request.client.host
    # Перевіряємо, чи досягнуто ліміту
    if not storage.hit(LIMIT, client_ip):
        raise HTTPException(
            status_code=429, detail="Request limit exceeded. Please try again later."
        )
    # Якщо ліміт не досягнуто, виконуємо запит далі
    response = await call_next(request)
    return response


@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}


# Запуск сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
