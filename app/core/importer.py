import json
from random import choice
import redis
red = redis.StrictRedis()
import asyncio

@asyncio.coroutine
def push_csv_to_worker(current_user, csv_input):

    for i, data_row in enumerate(csv_input):
        # print(type(csv_input))

        dic = {"product_name": data_row[0],
               "product_sku": data_row[1].lower(),
               "product_description": data_row[2],
               "product_is_active": choice([True, False])
               }

        current_user.launch_task('fill_product', 'running example', dic)
        red.publish('jobs', json.dumps(dic))