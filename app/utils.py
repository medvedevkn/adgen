from pydantic import BaseModel
from dataclasses import dataclass

class Buyer(BaseModel):
    name: str 
    surname: str
    password: str

@dataclass
class Query(BaseModel):
    keyword: str
    buyer: int

class User_Query(BaseModel):
    api: str
    keyword: str
    gen_id: int

@dataclass
class generation(BaseModel):
    gen_id: int
    buyer_id: int
    keyword: str
    event_dt: str
    response: str
    status: int
