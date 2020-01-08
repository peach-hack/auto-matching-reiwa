from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(String(128), primary_key=True, autoincrement=False)
    site = Column(String(10))
    profile_id = Column(String(128))
    profile_url = Column(String(200))
    name = Column(String(50))
    age = Column(String(10))
    title = Column(String(128))
    url = Column(String(200))
    image_url = Column(String(500))
    posted_at = Column(DateTime)
    genre = Column(String(20))
    prefecture = Column(String(10))
    city = Column(String(16))
    keyword = Column(String(16))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime,
                        nullable=False,
                        default=datetime.now,
                        onupdate=datetime.now)  # noqa

    def __repr__(self):
        return "<Post(id='{}', site='{}', profile_id='{}', name='{}', age='{}', title='{}', post_at='{}', genre='{}', prefecture='{}', city='{}', url='{}', image_url='{}')>".format(
            self.id, self.site, self.profile_id, self.name, self.age,
            self.title, self.post_at, self.genre, self.prefecture, self.city,
            self.url, self.image_url)
