import time
from contextlib import asynccontextmanager
import sentry_sdk
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from app.logger import logger
from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "metrics"],
)

instrumentator.instrument(app).expose(app)

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Authorization",
    ],
)

# @app.on_event("startup")
# def startup():
#     redis = aioredis.from_url("redis://localhost:6379")
#     FastAPICache.init(RedisBackend(redis), prefix="cache")


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
    return response


sentry_sdk.init(
    dsn=settings.SENTRY_DNS,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
