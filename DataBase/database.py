from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models



def _get_or_create(session, model, uniqe_field, data):
    instance: model = session.query(model).filter_by(**{uniqe_field: data[uniqe_field]}).first()

    if not instance:
        instance = model(**data)
    return instance


class Database:
    counter = 0

    def __init__(self, db_url):
        engine = create_engine(db_url)
        models.Base.metadata.create_all(bind=engine)
        self.maker = sessionmaker(bind=engine)

    def create_post(self, data):
        session = self.maker()
        post = _get_or_create(session, models.Post, "url", data["post_data"])
        author = _get_or_create(session, models.Author, "url",  data["author_data"])
        tags = [_get_or_create(session, models.Tag, "url", tag_data) for tag_data in data["tags_data"]]

        post.author = author
        post.tags.extend(tags)

        try:
            session.add(post)
            session.comit()
        except Exception as exc:
            print(exc)
            session.rollback()
        finally:
            self.counter += 1
            print(f"entry#{self.counter}")
            session.close()

