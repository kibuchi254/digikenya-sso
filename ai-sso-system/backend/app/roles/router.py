from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db
from app.roles.models import Role
from app.dependencies import get_current_active_user
from app.users.models import User
from pydantic import BaseModel

class RoleCreate(BaseModel):
    name: str
    permissions: str  # e.g., "read:users,write:tenants"

class RoleOut(BaseModel):
    id: int
    name: str
    permissions: str

    class Config:
        orm_mode = True

router = APIRouter()

@router.post("/", response_model=RoleOut)
async def create_role(role: RoleCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    # Check if user has permission to create roles (RBAC logic here)
    db_role = await db.execute(select(Role).where(Role.name == role.name))
    if db_role.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Role already exists")
    new_role = Role(name=role.name, permissions=role.permissions, tenant_id=current_user.tenant_id)
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return new_role

@router.get("/{role_id}", response_model=RoleOut)
async def get_role(role_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    role = await db.get(Role, role_id)
    if not role or role.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Role not found")
    return role