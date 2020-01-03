from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.post import Post

url = 'mysql+mysqldb://automatching:reiwa@localhost/auto_matching?charset=utf8'
engine = create_engine(url, echo=True)

post = Post(id='1', name="test", title="hello")

Session = sessionmaker(bind=engine)
session = Session()
session.add(post)
session.commit()

session.close()
