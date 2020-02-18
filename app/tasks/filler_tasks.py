import sqlalchemy
from redis import Redis
import rq
from sqlalchemy.dialects.postgresql import insert
from app.models import Product, Task
queue = rq.Queue('microblog-tasks', connection=Redis.from_url('redis://'))
from app import db
session = db.session

def fill_product(data_row):
    print('Starting task')
    get_or_create(session, data_row)
    print('Task completed')

def get_or_create(session, kwargs):

    try:
        instance = Product(product_name=kwargs['product_name'],
                           product_sku=kwargs['product_sku'],
                           product_description=kwargs['product_description'],
                           product_is_active=kwargs['product_is_active'])
        session.add(instance)
        session.commit()

    except sqlalchemy.exc.IntegrityError as exc:
        session.rollback()

        insert_stmt = insert(Product).values(
            product_name=kwargs['product_name'],
            product_sku=kwargs['product_sku'],
            product_description=kwargs['product_description'],
            product_is_active=kwargs['product_is_active'])

        do_update = insert_stmt.on_conflict_do_update(index_elements=['product_sku'], set_=kwargs)
        session.execute(do_update)