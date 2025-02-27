from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from src.fetch_api.database.models.base import Base


class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(127), nullable=False)
    body: Mapped[str] = mapped_column(String(255), nullable=False)

    @classmethod
    def default_order_by(cls):
        return [cls.id.desc()]

    def __repr__(self):
        return f"<Post(id={self.id}, user_id={self.user_id}, title={self.title}, body={self.body})>"
