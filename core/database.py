from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


engine = create_engine("sqlite:///orm_data.db", echo=True)


SessionLocal = sessionmaker(bind=engine)
