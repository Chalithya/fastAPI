from typing import Optional
from fastapi import FastAPI, Query
from enum import Enum
from pydantic import BaseModel





app = FastAPI()

@app.get("/")
async def root():
    return {"message", "Hello World"}



@app.get("/home")
async def root():
    return {"message", "This is Home"}



@app.get("/user/profile")
async def user_profile():
    return {"Message" : "This is user profile"}



@app.get("/user/{user_id}")
async def read_user(user_id: int):
    return {"user_id" : user_id}


""" This is a Enum class"""

class ModelVikings(str, Enum):
    floki = "floki"
    ragnar = "ragnar"
    bjorn = "bjorn"


@app.get("/vikings/{viking_name}")
async def get_vikings(viking_name: ModelVikings):
    if viking_name == ModelVikings.floki:
        return {"viking_name": viking_name, "message": "This is Floki the great"}
    if viking_name.value == "ragnar":
        return {"viking_name": viking_name, "message": "Great Ragnar"}

    return {"viking_name": viking_name, "message": "Hail Vikings"}



# ------- Path Converter ------------------------------------------------------------------

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


#------- Query Parameters -------------------------------------

items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/item/")
async def read_item(skip: int = 0, limit: int = 10):
    return items_db[skip: skip + limit]


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = Query(None, min_length=2, max_length=10)):
    if q:
        return {"item_id": item_id, "q:": q}
    
    return {"item_id": item_id}


#-------------------------Data Model-----------------------------

class Item_model(BaseModel):
    name: str
    price: float
    tax: Optional[float] = None



@app.put("/model/{item_id}")
async def create_model(item_id: str, item_model: Item_model):
    item_dict = item_model.dict()
    if item_model.tax:
        price_with_tax = item_model.price + item_model.tax
        item_dict.update({"price_with_tax": price_with_tax})


    return {"item_id": item_id, **item_dict}