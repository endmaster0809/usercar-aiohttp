import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)

__all__ = ['user', 'car']

meta = MetaData()

user = Table(
    'user', meta,

    Column('id', Integer, primary_key=True),
    Column('user_name', String(200), nullable=False),
    Column('email', String(200), nullable=False)
)

car = Table(
    'car', meta,

    Column('id', Integer, primary_key=True),
    Column('car_name', String(200), nullable=False),
)


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize']
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
