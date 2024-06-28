import datetime
from sqlalchemy import BigInteger, Integer, String,DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

import os
from dotenv import load_dotenv
load_dotenv()
engine = create_async_engine(url = os.getenv('SQLALCHEMY_URL'))# dbms driver

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    
    id = mapped_column(BigInteger,primary_key= True,unique=True)

class Threat(Base):
    __tablename__ = 'threat'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(666))
    rec_solve:Mapped[str] = mapped_column(String(2000))
    url:Mapped[str] = mapped_column(String(100))
    danger_level:Mapped[str] = mapped_column(String(300))

class Soft(Base):
    __tablename__='soft'

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(100))
    add_date = mapped_column(DateTime)
    __table_args__ = {'extend_existing': True}

class UsersSoft(Base):
    __tablename__='users_soft'

    id_user:Mapped[int] = mapped_column(ForeignKey('user.id'),primary_key=True)#fk
    id_soft:Mapped[int] = mapped_column(ForeignKey('soft.id'),primary_key=True)#fk
    choose_date = mapped_column(DateTime)
    is_active:Mapped[int] = mapped_column()


class SoftsThreat(Base):
    __tablename__='softs_threat'

    id_soft:Mapped[int] = mapped_column(ForeignKey('soft.id'),primary_key=True)#fk
    id_threat:Mapped[int] = mapped_column(ForeignKey('threat.id'),primary_key=True)#fk

class UsersThreat(Base):
    __tablename__='users_threat'

    id_user:Mapped[int] = mapped_column(ForeignKey('user.id'),primary_key=True)#fk
    id_threat:Mapped[int] = mapped_column(ForeignKey('threat.id'),primary_key=True)#fk
    send_date = mapped_column(DateTime)
    threat_status:Mapped[str] = mapped_column()
    threat_solution:Mapped[str] = mapped_column(String(2500), nullable = True)
    accept_date = mapped_column(DateTime,nullable = True)
    refuse_date= mapped_column(DateTime,nullable = True)
    solve_date= mapped_column(DateTime,nullable = True)

class UsersApplication(Base):
    __tablename__='users_application'

    id_application:Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name:Mapped[str] = mapped_column(String(50))
    application_date = mapped_column(DateTime)


async def async_main():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
