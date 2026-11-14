from typing import TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound=DeclarativeBase)


class BaseRepo:
    model: type[T]

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> T:
        obj = cls.model(**kwargs)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[T]:
        result = await session.execute(select(cls.model))
        return result.scalars().all()

    @classmethod
    async def get_all_by_kwargs(
        cls, session: AsyncSession, **kwargs: dict
    ) -> T | None:
        result = await session.execute(select(cls.model).filter_by(**kwargs))
        return result.scalars().all()

    @classmethod
    async def get_one_by_id(cls, session: AsyncSession, id_: int) -> T | None:
        result = await session.execute(
            select(cls.model).where(cls.model.id == id_)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_one_by_kwargs(
        cls, session: AsyncSession, **kwargs: dict
    ) -> T | None:
        result = await session.execute(select(cls.model).filter_by(**kwargs))
        return result.scalar_one_or_none()

    @classmethod
    async def update_by_id(cls, session: AsyncSession, id_: int, **kwargs) -> T:
        await session.execute(
            update(cls.model).where(cls.model.id == id_).values(**kwargs)
        )
        await session.commit()

        result = await session.execute(
            select(cls.model).where(cls.model.id == id_)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id_: int) -> None:
        await session.execute(delete(cls.model).where(cls.model.id == id_))
        await session.commit()
