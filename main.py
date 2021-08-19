from typing import Optional
from fastapi import FastAPI, Query, Body
from enum import Enum
from fastapi.param_functions import Body, Path
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


    #---------------- String validation ----------------------
""" 
Regex -> In regex it cheks the input is according to the format '^' the starting point '$' denotes ending point
alias -> can be used to declasre variables which are not valid in python
depricate -> is used to tell that try not to use this
"""



@app.get("/item1/")
async def read_items(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="q string",
        description="Description of q",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results



#------------------------------Path parameter -------------------------------------

@app.get("/item2/{item_id}")
async def read_items(
    q: str,
    item_id: int = Path(..., title="Id of the item id", ge=1, le=9999999)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    
    return results

"""-------------------------This part is related to body-------------------------------"""
#--------------------------- Body Multiple parameter -------------------------------

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None



class User(BaseModel):
    username: str
    full_name: Optional[str] = None



@app.put("/item3/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results3 = {"item_id": item_id, "item": item, "user": user}
    return results3



@app.put("/item4/{tiem_id}")
async def update_item(item_id: int, item: Item, user: User, importance: int = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


