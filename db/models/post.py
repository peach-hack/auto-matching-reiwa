from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

url = 'mysql+mysqldb://automatching:reiwa@localhost/auto_matching?charset=utf8'
engine = create_engine(url, echo=True)
Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=False)
    site = Column(String(10))
    profile_id = Column(Integer)
    name = Column(String(50))
    age = Column(String(10))
    title = Column(String(50))
    url = Column(String(200))
    image_url = Column(String(500))
    post_at = Column(String(20))
    genre = Column(String(20))
    prefecture = Column(String(10))
    city = Column(String(10))

    def __repr__(self):
        return "<Post(id='{}', site='{}', profile_id='{}', name='{}', age='{}', title='{}', post_at='{}', genre='{}', prefecture='{}', city='{}', url='{}', image_url='{}')>".format(
            self.id, self.site, self.profile_id, self.name, self.age,
            self.title, self.post_at, self.genre, self.prefecture, self.city,
            self.url, self.image_url)


Base.metadata.create_all(engine)
