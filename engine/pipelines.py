from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.post import Post
from .constants.db import DB_URL


class MysqlPipeline(object):
    def open_spider(self, spider):
        engine = create_engine(DB_URL, echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        post = Post(id=item['id'],
                    site=item['site'],
                    profile_id=item['profile_id'],
                    name=item['name'],
                    age=item['age'],
                    title=item['title'],
                    url=item['url'],
                    image_url=item['image_url'],
                    posted_at=item['posted_at'],
                    genre=item['genre'],
                    prefecture=item['prefecture'],
                    city=item['city'],
                    profile_url=item['profile_url'],
                    keyword=item['keyword'])
        self.session.merge(post)
        self.session.commit()
        return item
