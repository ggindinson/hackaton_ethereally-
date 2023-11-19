# Created by https://t.me/vlasovdev models file | Создано https://t.me/vlasovdev models file


import datetime
from typing import Any, Dict, List, Sequence, Type, TypeVar

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum,
    ForeignKey,
    and_,
    delete,
    func,
    select,
    update,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    registry,
    relationship,
)

from database.custom_types import bigint, bigint_array
from typings.consts import USERS_RATING_LIMIT
from typings.enums import RoleEnum
from utils.datetime_utils import current_datetime_with_tz
from utils.helpers import PrettyRepr

T = TypeVar("T")


# Define declarative base
class Base(DeclarativeBase, PrettyRepr):
    __table_args__ = {"extend_existing": True}
    __abstract__ = True

    registry = registry(
        type_annotation_map={
            bigint: BigInteger,
            bigint_array: ARRAY(BigInteger),
        }
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=current_datetime_with_tz()
    )

    @classmethod
    async def get_by_id(
        cls: Type[T], session: AsyncSession, model_id: int | str
    ) -> T | None:
        row = await session.execute(select(cls).where(cls.id == model_id))
        return row.scalar_one_or_none()

    @classmethod
    async def get_all(cls: Type[T], session: AsyncSession) -> Sequence[T]:
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def create(
        cls: Type[T],
        session: AsyncSession,
        params: List[Dict[str, Any]] | Dict[str, Any],
    ) -> T:
        stmt = pg_insert(cls).values(params).on_conflict_do_nothing().returning(cls)
        result = await session.execute(stmt)

        await session.commit()
        return result.scalar()

    @classmethod
    async def update(
        cls: Type[T], session: AsyncSession, model_id: int | str, **kwargs: Any
    ) -> T:
        result = await session.execute(
            update(cls).where(cls.id == model_id).values(**kwargs).returning(cls)
        )
        await session.commit()
        return result.scalar()

    @classmethod
    async def updateall(cls: Type[T], session: AsyncSession, **kwargs: Any) -> T:
        result = await session.execute(update(cls).values(**kwargs).returning(cls))
        await session.commit()
        return result.scalar()

    @classmethod
    async def delete(cls, session: AsyncSession, model_id: int | str | None = None):
        statement = delete(cls)
        if model_id:
            statement = statement.where(cls.id == model_id)

        await session.execute(statement)
        return await session.commit()

    @classmethod
    async def deletemany(cls, session: AsyncSession, model_ids: List[int | str]):
        statement = delete(cls).where(cls.id.in_(model_ids))

        await session.execute(statement)
        return await session.commit()

    @classmethod
    async def count(
        cls, session: AsyncSession, extra_where_clauses: List[Any] | None = None
    ) -> int:
        statement = select(func.count(cls.id))
        if extra_where_clauses:
            statement = statement.where(and_(*extra_where_clauses))
        return (await session.execute(statement)).scalar()


class AssociationTable(Base):
    __tablename__ = "associations"

    id: Mapped[bigint] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[bigint] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))

    @classmethod
    async def delete_row(cls, session: AsyncSession, user_id: int, event_id: int):
        statement = delete(AssociationTable).where(
            and_(
                AssociationTable.user_id == user_id,
                AssociationTable.event_id == event_id,
            )
        )

        await session.execute(statement)
        await session.commit()


class Users(Base, PrettyRepr):
    __tablename__ = "users"

    id: Mapped[bigint] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default="")
    username: Mapped[str] = mapped_column(default="")
    points: Mapped[int] = mapped_column(default=0)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.USER)
    events: Mapped[List["Events"]] = relationship(
        lazy="selectin",
        secondary=AssociationTable.__table__,
        back_populates="users",
    )
    last_activity: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=current_datetime_with_tz()
    )

    @classmethod
    async def get_rating(cls, session: AsyncSession) -> List["Users"]:
        statement = (
            select(Users).order_by(Users.points.desc()).limit(USERS_RATING_LIMIT)
        )

        result = await session.execute(statement)

        return result.scalars().all()


class Events(Base, PrettyRepr):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default="")
    description: Mapped[str] = mapped_column(default="")
    creator: Mapped[bigint] = mapped_column(ForeignKey(Users.id))

    users: Mapped[List["Users"]] = relationship(
        lazy="selectin",
        secondary=AssociationTable.__table__,
        back_populates="events",
    )
