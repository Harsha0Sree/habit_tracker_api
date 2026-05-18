from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Habit(Base):
    __tablename__ = "habits"
    habit_name: Mapped[str] = mapped_column(unique=True)
    id: Mapped[int] = mapped_column(primary_key=True)
