from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db
from app.users.models import User
from app.users.schema import UserCreate, UserOut
from app.users.service import create_user
from app.dependencies import get_current_active_user
from app.auth.password_handler import hash_password
from app.utils.email import send_activation_email

router = APIRouter()

@router.post("/", response_model=UserOut)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await db.execute(select(User).where(User.email == user.email))
    if db_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = await create_user(db, user.email, hashed_password, user.first_name, user.last_name)
    await send_activation_email(new_user.email)
    return new_user

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/activate/{user_id}")
async def activate_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = True
    await db.commit()
    await db.refresh(user)
    return {"message": "User activated"}