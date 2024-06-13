import sys
import redis
import datetime
import time
from redis import Redis
import requests

sys.path.append('..')
from database_handler import insert_new_generation
from config import *

connection = Redis(**redis_conn)

def create_generation_request(id, keyword):
    cur_prompt = handle_prompt(keyword)
    post_q["text"] = cur_prompt
    r = requests.post(url=url, json=post_q)
    return r

len = connection.llen("queue")

while True:
    if connection.llen("queue") == 0:
        time.sleep(2.5)
        continue
    message = connection.rpop("queue")
    if message:
        m = message.decode()
        cur_message = eval(m)
        r = create_generation_request(cur_message['gen_id'], cur_message['keyword'])
        if r.status_code == 200:
            insert_new_generation(cur_message['gen_id'], 1, cur_message['keyword'], cur_message['buyer_id'],  r.content, str(datetime.datetime.now())[:19])
    time.sleep(0.5)

