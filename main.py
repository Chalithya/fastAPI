from fastapi import FastAPI
from enum import Enum






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