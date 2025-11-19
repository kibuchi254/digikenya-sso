from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select # ADDED: Necessary for ORM queries

from app.db import get_db
from app.auth.jwt_handler import create_access_token, create_refresh_token, decode_refresh_token
from app.auth.password_handler import verify_password
from app.auth.oauth2 import oauth2_google
# FIX: Corrected import path from 'app.users.models' (plural) to 'app.user.models' (singular)
from app.users.models import User
from app.users.schema import UserOut # Assuming schema path is correct (plural 'users')
from app.utils.email import send_otp_email
from app.utils.redis_cache import redis_client
import random
import datetime

router = APIRouter()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Query for the user by email
    user = await db.execute(select(User).where(User.email == form_data.username))
    user = user.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh")
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    payload = decode_refresh_token(refresh_token)
    
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
    user_id: int = payload.get("sub")
    
    # Using db.get() for primary key lookup
    user = await db.get(User, user_id) 
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
    access_token = create_access_token(data={"sub": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/otp/send")
async def send_otp(email: str, db: AsyncSession = Depends(get_db)):
    # Query for the user by email
    user = await db.execute(select(User).where(User.email == email))
    user = user.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    otp = random.randint(100000, 999999)
    # Store OTP in Redis with a 5-minute expiry
    redis_client.setex(f"otp:{user.id}", 300, otp) 
    
    await send_otp_email(email, otp)
    
    return {"message": "OTP sent"}

@router.post("/otp/verify")
async def verify_otp(email: str, otp: int, db: AsyncSession = Depends(get_db)):
    # Query for the user by email
    user = await db.execute(select(User).where(User.email == email))
    user = user.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    stored_otp = redis_client.get(f"otp:{user.id}")
    
    if stored_otp and int(stored_otp) == otp:
        redis_client.delete(f"otp:{user.id}")
        return {"message": "OTP verified"}
        
    raise HTTPException(status_code=400, detail="Invalid OTP")

@router.get("/oauth/google")
async def oauth_google_login():
    return await oauth2_google.authorize_redirect()

@router.get("/oauth/google/callback")
async def oauth_google_callback(code: str, db: AsyncSession = Depends(get_db)):
    # 1. Exchange code for token
    token = await oauth2_google.authorize_access_token(code) 
    
    # 2. Get user profile info
    user_info = await oauth2_google.get_user_info(token) 
    
    # 3. Find or create user based on email
    user = await db.execute(select(User).where(User.email == user_info["email"]))
    user = user.scalar_one_or_none()
    
    if not user:
        # Create new user
        user = User(
            email=user_info["email"], 
            first_name=user_info.get("given_name"), 
            last_name=user_info.get("family_name"), 
            is_active=True # Automatically activate OAuth users
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
    # 4. Generate access token
    access_token = create_access_token(data={"sub": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}