import datetime
from peewee import *
from playhouse.flask_utils import object_list, PaginatedQuery

db = SqliteDatabase('data.db')


class BaseModel(Model):
    class Meta:
        database = db


class LastSize(BaseModel):
    product_id = BigIntegerField()
    owner_id = TextField()
    photo_id = BigIntegerField()


class ActualFees(LastSize):
    pass


class AlbumVk(LastSize):
    create_at = TextField()


class TokenVK(BaseModel):
    id = IntegerField()
    token = TextField()
    created_at = TextField()
