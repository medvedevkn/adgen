import redis
from config import redis_conn
from redis import Redis
from pydantic import BaseModel


connection = Redis(**redis_conn)

def add_new_task(data, con=connection):
    con.lpush("queue", data)
    return connection.llen("queue")

