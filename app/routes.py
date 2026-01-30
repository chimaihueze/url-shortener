import random
import string
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select, update

from app.core.db.session import get_session
from app.model import URL
from app.schema import RequestDTO, ResponseDTO, SuccessResponse, StatResponseDTO
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="")

@router.post("", response_model=SuccessResponse[ResponseDTO], status_code=201)
async def shorten(data: RequestDTO, db: AsyncSession = Depends(get_session)):
    
    short_code = "".join(random.choices(string.ascii_lowercase, k=7))
    record = URL(url=str(data.url), short_code=short_code)

    db.add(record)
    await db.commit()
    await db.refresh(record)

    return SuccessResponse(
        message="url shortened successfully",
        data=ResponseDTO.model_validate(record)
    )

@router.get("/{short_code}", response_model=SuccessResponse[ResponseDTO], status_code=200)
async def get_original_url(short_code: str, db: AsyncSession = Depends(get_session)):
    
    stmt = select(URL).where(URL.short_code == short_code)

    result = await db.execute(stmt)

    url_data = result.scalar_one_or_none()

    if not url_data:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found",
        )
    stmt = (
        update(URL)
        .where(URL.short_code == short_code)
        .values(access_count=URL.access_count + 1)
        .returning(URL)
    )

    result = await db.execute(stmt)
    await db.commit()

    url_data = result.scalar_one()

    return SuccessResponse(
            message="original url retrieved successfully",
            data=ResponseDTO.model_validate(url_data)
        )

@router.put("/{short_code}", response_model=SuccessResponse[ResponseDTO], status_code=200)
async def update_original_url(short_code: str, data: RequestDTO, db: AsyncSession = Depends(get_session)):
    stmt = select(URL).where(URL.short_code == short_code)

    result = await db.execute(stmt)

    url_data = result.scalar_one_or_none()

    if not url_data:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found",
        )

    url_data.url = str(data.url)
    db.add(url_data)
    await db.commit()
    await db.refresh(url_data)

    return SuccessResponse(
        message="URL updated successfully",
        data=ResponseDTO.model_validate(url_data)
    )

@router.delete("/{short_code}", status_code=204)
async def delete_url(short_code: str, db: AsyncSession = Depends(get_session)):
    stmt = select(URL).where(URL.short_code == short_code)
    result = await db.execute(stmt)
    url_data = result.scalar_one_or_none()

    if not url_data:
        raise HTTPException(status_code=404, detail="Short URL not found")

    await db.delete(url_data)
    await db.commit()

    return Response(status_code=204)


@router.get("/{short_code}/stats", response_model=SuccessResponse[StatResponseDTO], status_code=200)
async def get_url_stats(short_code: str, db: AsyncSession = Depends(get_session)):
    stmt = select(URL).where(URL.short_code == short_code)
    result = await db.execute(stmt)
    stat_data = result.scalar_one_or_none()

    if not stat_data:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return SuccessResponse(
        message="url stats retrieved successfully",
        data=StatResponseDTO.model_validate(stat_data)
    )