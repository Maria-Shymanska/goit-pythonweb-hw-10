from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.api.const.contacts import contacts
from src.database.db import get_db

router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.scalar_one_or_none()

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


# To comment after seeder working out
@router.get("/start-seeder")
async def run_seeder(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        db.add_all(contacts)
        await db.commit()
        return {"message": "Database seeded successfully!"}