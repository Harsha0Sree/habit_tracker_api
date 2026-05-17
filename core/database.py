from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Habit(Base):
    __tablename__ = "habits"
    habit_name: Mapped[str] = mapped_column(unique=True)
    id: Mapped[int] = mapped_column(primary_key=True)


engine = create_engine("sqlite:///orm_data.db",echo=True)
Base.metadata.create_all(engine)

habit1 = Habit(habit_name="fuck_you1")
habit2 = Habit(habit_name="fuck_you3")
habit3 = Habit(habit_name="fuck_you2")

with Session(engine) as session:
    try:
        session.add_all([habit2, habit1, habit3])
        session.commit()

    except IntegrityError:
        session.rollback()
        print("dupe habit")
    row = select(Habit).where(Habit.habit_name == "fuck_you1")
    result = session.execute(row).scalar_one_or_none()
    if result is not None:
        session.delete(result)
        session.commit()

    else:
        print("no data exists")

    query_all_rows = select(Habit)
    all_rows = session.execute(query_all_rows).scalars().all()
    for habit in all_rows:
        print(habit.habit_name, habit.id)

