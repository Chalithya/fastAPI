from typing import Optional, List, Union
from fastapi import FastAPI, Query, Body, Header, status, File, UploadFile, Form
from enum import Enum
from fastapi.param_functions import Body, Path
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse






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



@app.put("/item4/{item_id}")
async def update_item(item_id: int, item: Item, user: User, importance: int = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


#--------------------------- Body Fields -------------------------------

class Itemnew(BaseModel):
    name: str
    description: Optional[str] = Field(None, title="The description of the item", max_length=300, min_length=1 )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None

    



@app.put("/item5/{item_id}")
async def update_item5(item_id: int, itemnew: Itemnew = Body(..., embed=True)):
    results5 = {"item_id": item_id, "item": itemnew}
    return results5



#--------------------------- Example Data  -------------------------------
class Item5(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }



class Item5_1(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)



@app.put("/items5_1/{item5_id}")
async def update_item(item5_id: int, item5: Item5):
    results = {"item5_id": item5_id, "item5": item5}
    return results



#--------------------------- Path operation configeration - Header  -------------------------------

@app.get("/item6/")
async def read_items(x_token: Optional[List[str]] = Header(None)):
    return {"X-Token values": x_token}



#--------------------------- Response Model  -------------------------------

class UserIn(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None



class UserOut(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.post("/newuser/", response_model=UserOut)
async def create_user(user: UserIn):
    return user



#---------------- Exclude default model --------------------------

class Item7(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items7 = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}



""" Can use both response_model_include and response_model_exclude """

@app.get("/item7/{item7_id}", response_model=Item7, response_model_exclude_unset=True)
async def read_item(item7_id: str):
    return items7[item7_id]



#---------------- Extra model --------------------------


# user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
# user_dict = user_in.dict()
# print(user_dict)


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items8 = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


# @app.get("/items8/{item_id}", response_model = Union[PlaneItem, CarItem])
# async def read_item(item_id: str):
#     return items8[item_id]

class Item8(BaseModel):
    name: str
    description: str


items8 = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

@app.get("/items8/", response_model=List[Item8], status_code=status.HTTP_201_CREATED)
async def read_items():
    return items8



#---------------- Request Files --------------------------


# @app.post("/files/")
# async def create_file(file: bytes = File(...)):
#     return {"file_size": len(file)}

"""
This is the best way for larger files and also usefull as we can get metadata from the file using this method
"""
# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):
#     return {"filename": file.filename}

"""
We can use lists of files to upload
"""

@app.post("/filesu/")
async def create_file(file: List[bytes] = File(...)):
    return {"file_size": len(file)}

@app.post("/uploadfilesu/")
async def create_upload_file(file: List[UploadFile] = File(...)):
    return {"filename": file.filename}



@app.get("/filehome/")
async def main():
    content = """
<body>
<form action="/filesu/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfilesu/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)



#---------------- Request Files --------------------------

@app.post("/fileup/")
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "filea_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }