from app.users.models import User

async def create_user(db, email, hashed_password, first_name=None, last_name=None):
    user = User(email=email, hashed_password=hashed_password, first_name=first_name, last_name=last_name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user