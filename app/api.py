# app/api.py
import json
from fastapi import FastAPI, Request, Body, Depends
from app.model import UserSchema, UserLoginSchema
from app.auth.auth_handler import signJWT
from app.auth.auth_bearer import JWTBearer
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# membuka file menu.json
with open("menu.json", "r") as read_file: 
    data = json.load(read_file)


# menampung nama user.
users = [ 
    {
    "fullname": "Anita Satria Dewi Fina",
    "username": "asdf",
    "password": "asdf"
    }
]

app = FastAPI() 


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {
        "page": "Home page"
    }
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {'Menu' : 'Item'}


# menghasilkan semua data dalam menu.json
@app.get('/menu', tags=['CRUD Menu']) 
async def read_all_menu() -> dict: 
    return data
 

# membaca 1 data dalam menu.json
@app.get('/menu/{item_id}', tags=['CRUD Menu'])
async def read_menu(item_id: int) -> dict:
    if item_id > len(data['menu']):
        return {
            "error": "No such menu with the supplied ID."
        }

    for menu_item in data['menu']:
        if menu_item["id"] == (item_id):
            return menu_item


# menambahkan menu
@app.post('/menu', dependencies=[Depends(JWTBearer())], tags=['CRUD Menu'])
async def Add_menu(name: str) ->dict: 
    id=1
    if(len(data["menu"])>0):
        id=data["menu"][len(data["menu"])-1]["id"]+1
    new_data={'id':id,'name':name}
    data['menu'].append(dict(new_data))

    #melakukan rewrite
    read_file.close()
    with open("menu.json","w") as write_file:
        json.dump(data,write_file,indent=4)
    write_file.close()
    return {
        "data": "post added."
    }


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.username)


def check_user(data: UserLoginSchema):
    for user in users:
        if user["username"] == data.username and user["password"] == data.password:
            return True
    return False


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.username)
    return {
        "error": "Wrong login details!"
    }


# menghasilkan semua nama user
@app.get('/user', tags=["user"]) 
async def read_all_user(): 
    return users


# mengupdate menu
@app.put('/menu/{item_id}', dependencies=[Depends(JWTBearer())], tags=['CRUD Menu'])
async def update_menu(item_id: int, name: str): 
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            menu_item['name']= name
            read_file.close()
            with open("menu.json","w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()
            return{"message":"Data berhasil diupdate"}
        else :
            return{"message":"Data tidak ditemukan."}


# menghapus salah satu menu
@app.delete('/menu/{item_id}', dependencies=[Depends(JWTBearer())], tags=['CRUD Menu'])
async def delete_menu(item_id: int, name: str): 
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            if menu_item['name'] == name:
                remove_data={'id':item_id,'name':name}
                data['menu'].remove(dict(remove_data))
                # rewrite menu.json
                read_file.close()
                with open("menu.json","w") as write_file:
                    json.dump(data,write_file,indent=4)
                write_file.close()
                return{"message":"Data berhasil dihapus"}
            else :
                return {"message":"Error : data tidak sesuai. Perhatikan nomor dan nama menu harus sesuai"}
    else :
        return {"message":"Error : Data tidak ditemukan."}




