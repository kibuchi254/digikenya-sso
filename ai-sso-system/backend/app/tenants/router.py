from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db
from app.tenants.models import Tenant
from pydantic import BaseModel

class TenantCreate(BaseModel):
    name: str
    description: str

class TenantOut(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True

router = APIRouter()

@router.post("/", response_model=TenantOut)
async def create_tenant(tenant: TenantCreate, db: AsyncSession = Depends(get_db)):
    db_tenant = await db.execute(select(Tenant).where(Tenant.name == tenant.name))
    if db_tenant.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Tenant already exists")
    new_tenant = Tenant(name=tenant.name, description=tenant.description)
    db.add(new_tenant)
    await db.commit()
    await db.refresh(new_tenant)
    return new_tenant

@router.get("/{tenant_id}", response_model=TenantOut)
async def get_tenant(tenant_id: int, db: AsyncSession = Depends(get_db)):
    tenant = await db.get(Tenant, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant