from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.tenants.router import router as tenants_router
from app.roles.router import router as roles_router
from app.health import router as health_router

from app.db import engine, Base

app = FastAPI(title="AI SSO System")

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(tenants_router, prefix="/tenants", tags=["tenants"])
app.include_router(roles_router, prefix="/roles", tags=["roles"])
app.include_router(health_router)

# Create tables on startup (for development; use Alembic in production)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)