from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Float, Integer, Date, Enum
from datetime import date
from typing import List
from sqlalchemy.orm import relationship
import enum


class Base(DeclarativeBase):
    pass


class GenderEnum(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class UserBase(Base):
    __tablename__ = "users"
    """
    TODO
    сделать вес, город, рост либо обяательными либо опциональным, с одной стороны суть приложения
    что б пользователь ввел это все, но с другой стороны, а если он захочет просто зайти и посмотреть что за фигня тут
    в таком случае он данные не заполнит, а приложуха покажет ему средние нормы людей и все
    в будущем либо продумать либо исправть
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    activity_minutes: Mapped[int] = mapped_column(Integer, default=0)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    water_goal: Mapped[int] = mapped_column(Integer)
    calorie_goal: Mapped[int] = mapped_column(Integer)
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum), nullable=False)
    water_logs: Mapped[List["WaterLog"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    food_logs: Mapped[List["FoodLog"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    workout_logs: Mapped[List["WorkoutLog"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User id {self.id} and city = {self.city}"


class WaterLog(Base):
    __tablename__ = "water_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    log_date: Mapped[date] = mapped_column(Date, default=date.today)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped["UserBase"] = relationship(back_populates="water_logs")

    def __repr__(self) -> str:
        return f"waterlog id  = {self.id} and logdate {self.log_date}"


class FoodLog(Base):
    __tablename__ = "food_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    log_date: Mapped[date] = mapped_column(Date, default=date.today)
    food_name: Mapped[str] = mapped_column(String(100), nullable=False)
    calories: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["UserBase"] = relationship(back_populates="food_logs")

    def __repr__(self) -> str:
        return f"foodlog id = {self.id} and log_date = {self.log_date}"


class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    log_date: Mapped[date] = mapped_column(Date, default=date.today)
    workout_type: Mapped[str] = mapped_column(String(50), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    burned_calories: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["UserBase"] = relationship(back_populates="workout_logs")

    def __repr__(self) -> str:
        return f"workoutlog id = {self.id} and date = {self.log_date}"
