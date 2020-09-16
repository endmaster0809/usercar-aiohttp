from sqlalchemy import create_engine, MetaData

from usercar.settings import config
from usercar.db import user, car

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[user, car])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(user.insert(), [
        {'user_name': 'user1',
         'email': 'user1@usercar.com'}
    ])
    conn.execute(car.insert(), [
        {'car_name': 'car1'},
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
