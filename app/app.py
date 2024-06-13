from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from rq import Queue
from database_handler import *
from utils import User_Query
from typing import Annotated
from publisher import add_new_task
import datetime
import time
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/imgs", StaticFiles(directory="imgs"), name="images")

templates=Jinja2Templates(directory="templates")

# create a route
@app.get("/")
async def index(request:Request):
    keys = init_keys()
    if len(keys) == 0:
        print("Something goes wrong with key loading")
    return templates.TemplateResponse("base.html", {"request":request})


@app.post("/postdata")
async def postdata(user_query:User_Query):
    if user_query.api not in init_keys():
        return {"message": f"Ваш API ключ не найден в базе"}
    id = get_buyer_id(user_query.api)
    gen_id = get_actual_gen_id()
    user_query.gen_id = gen_id + 1
    cur_dt = str(datetime.datetime.now())[:19]
    cur_ln = add_new_task(str({"gen_id": gen_id + 1, "buyer_id": id, "keyword": user_query.keyword, "event_dt": cur_dt}))
    insert_new_query(gen_id + 1, id, user_query.keyword, cur_dt)
    time_spent = get_time_spent()
    return {"message": f"API ключ валиден.\nВаш запрос по ключевому слову {user_query.keyword} {cur_ln} в очереди.\nПримерное время ожидания: {str(int(cur_ln) * int(time_spent))} секунд", "cur_gen_id": gen_id + 1}


@app.post("/check")
async def check(user_query:User_Query, timeout=50):
    cur_time = 1
    while True and cur_time < timeout:
        response = get_gen_result(user_query.gen_id)
        if response == 0:
            time.sleep(1)
            cur_time += 1
        else:
            return {"message": response}

@app.post("/like")
async def like(user_query:User_Query):
    insert_feedback(user_query.gen_id, 1)
    return {"message": "Хорошо"}
        
@app.post("/dislike")
async def dislike(user_query:User_Query):
    insert_feedback(user_query.gen_id, 0)
    return {"message": "Плохо"}