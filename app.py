from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#Para tipos de datos no definidos en pydatinc
from typing import Text
#Importar paquete pora trabajar con fechas
from datetime import datetime
#Biblioteca para generar id automáticos
from uuid import uuid4 as uuid

app = FastAPI()

posts = []
#Post Model, clase Post que hereda de BaseModel para definir la estructura de cada post
class Post(BaseModel):
    id: str | None = None
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: datetime | None = None
    published: bool = False

@app.get("/")
def read_root():
    return {"message": "Hello from REST API"}

@app.get("/posts", response_model=Post)
def get_posts():
    return posts    

@app.post("/create", response_model=Post)
def create_post(post: Post):
    #asigno el id antes de guardar el post
    #print(uuid())
    post.id = str(uuid())
    #.model_dump() convierte cada post en un diccionario de pyton con la estructura clave:valor
    posts.append(post.model_dump())
    return post

@app.get("/posts/{id}", response_model=Post)
def get_post(id: str):
    for post in posts:
        if post["id"] == id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")
    
@app.delete("/posts/{id}")
def delete_post(id: str):
    for index, post in enumerate(posts):
        if post["id"] == id:
            posts.pop(index)
            return {"message": "Post removed"}
    raise HTTPException(status_code=404, detail="Post not found")

@app.put("/posts/{id}")
def update_post(id: str, updated_post:Post):
    for index, post in enumerate(posts):
        if post["id"] == id:
            posts[index]["title"]=updated_post.title
            posts[index]["content"]=updated_post.content
            posts[index]["author"]=updated_post.author
            return {"message": "Post updated"}
    raise HTTPException(status_code=404, detail="Post not found")
 

        
    
    


