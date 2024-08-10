from sqlalchemy import Integer, String, Column, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from ..database import base
from sqlalchemy.orm import relationship


class Movie(base):
    __tablename = "movies"

    id = Column(Integer, primary_key=True, nullable=False)
    movie_title = Column(String, nullable=False, unique=True)
    review = Column(String, nullable=False)
    rating = Column(Integer, default=0)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
