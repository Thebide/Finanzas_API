from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class BaseModel(DeclarativeBase):
    __abstract__ = True

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created : Mapped[datetime] = mapped_column(default= datetime.now, nullable=False)
    update : Mapped[datetime] = mapped_column(default= datetime.now, nullable=False, onupdate=datetime.now)