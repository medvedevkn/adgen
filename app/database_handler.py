import psycopg2 as pg
from config import *
import requests

def init_keys()->list:
    try:
        con = pg.connect(**pg_conn)
        cursor = con.cursor()
        cursor.execute(query)
        return [row[0].lower() for row in cursor.fetchall()]
    except Exception:
        print("Something goes wrong with pg connection")
        return []
    

def get_buyer_id(api_str)->int:
    try:
        con = pg.connect(**pg_conn)
        cursor = con.cursor()
        cursor.execute(query_buyer)
        return  [row[0] for row in cursor.fetchall()][0]
    except Exception:
        print("Something goes wrong with pg connection")
        return 0


def get_actual_gen_id()->int:
    try:
        con = pg.connect(**pg_conn)
        cursor = con.cursor()
        cursor.execute(query_gen)
        res = [row[0] for row in cursor.fetchall()][0]
        return res
    except Exception:
        print("Something goes wrong with pg connection")
        return 0
    

def get_time_spent():
    try:
        con = pg.connect(**pg_conn)
        cursor = con.cursor()
        cursor.execute(time_spent)
        result = cursor.fetchone()
        return result[0]
    except Exception:
        print("Something goes wrong with pg connection read time")
        return 0
    

def insert_new_query(gen_id, buyer_id, keyword, event_dt):
    try:
        con = pg.connect(**pg_conn)
        cursor = con.cursor()
        cursor.execute(query_gen_update, (gen_id, buyer_id, keyword, event_dt))
        con.commit()
    except Exception:
        print("Something goes wrong with pg connection")
        return 0   
    
def insert_feedback(gen_id, val):
    try:
        con = pg.connect(**pg_conn)
        cursor = con.cursor()
        cursor.execute(feed_insert, (gen_id, val))
        con.commit()
    except Exception:
        print("Something goes wrong with pg connection")
        return 0   


def insert_new_generation(gen_id, model_id, buyer_id, keyword, response, event_dt):
    try:
        con = pg.connect(**pg_conn)
        cursor = con.cursor()
        cursor.execute(gen_insert, (gen_id, model_id, buyer_id, keyword, response.decode('utf-8'), event_dt))
        con.commit()
    except Exception:
        print("Something goes wrong with pg connection insert")
  

def get_gen_result(gen_id):
    try:
        con = pg.connect(**pg_conn)
        cursor = con.cursor()
        cursor.execute(gen_result, (gen_id,))
        result = cursor.fetchone()
        if result is None or len(result) == 0:
            return 0
        return result
    except Exception:
        print("Something goes wrong with pg connection read")
        return 0
    