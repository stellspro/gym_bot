from sqlalchemy import select
from app.database.database import db
from app.database.database import Base


class BaseRepository:
    model = Base

    def __init__(self, db: db):
        self.session = db

    def get(self, id: int):
        if id:
            stmt = select(self.model).where(self.model.id == id)
            entity = self.session.scalar(stmt)
            return entity

    def get_by_name(self, name: str):
        stmt = select(self.model).where(self.model.name == name)
        entity = self.session.scalar(stmt)
        return entity

    def all(self):
        stmt = select(self.model)
        entities = [a for a in self.session.scalars(stmt)]
        return entities
