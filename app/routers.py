from datetime import datetime
import random
import string
from fastapi import APIRouter, Depends

from app.core.db.session import get_session
from app.model import URL
from app.schema import RequestDTO, ResponseDTO, SuccessResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="")

@router.post("", response_model=SuccessResponse[ResponseDTO], status_code=201)
async def shorten(data: RequestDTO, db: AsyncSession = Depends(get_session)):
    
    short_code = "".join(random.choices(string.ascii_lowercase, k=7))
    created_at = datetime.now()
    record = URL(url=str(data.url), short_code=short_code, created_at=created_at)

    db.add(record)
    await db.commit()
    await db.refresh(record)

    return SuccessResponse(
        message="url shortened successfully",
        data=ResponseDTO.model_validate(record)
    )