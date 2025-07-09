from fastapi import FastAPI, Form
from typing import Annotated
import mariadb
import os
import httpx
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:80",
    "http://127.0.0.1:80",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/tset")
def test(a:int):
    return {"a변수":a}

@app.get("/test2")
def test2(문자:str):
    return {"문자열":문자}

@app.post("/po1")
def po1(a: Annotated[str, Form(...)]):
    return {"respon": "post 요청 성공!" , "a변수":a}

@app.get("/db")
def db():
    conn_params={
        "user": os.getenv('MARIADB_USER', 'root'),
        "password": os.getenv('MARIADB_PASSWORD'),
        "host": os.getenv('MARIADB_HOST'),
        "port": int(os.getenv('MARIADB_PORT')),
        "database": os.getenv('MARIADB_DATABASE')
    }
    conn= mariadb.connect(**conn_params)
    cur = conn.cursor()
    sql = "SELECT * FROM movies"
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return {"movies": result}

@app.get("/year")
async def year(y:str):
    conn_params={
        "user": os.getenv('MARIADB_USER', 'root'),
        "password": os.getenv('MARIADB_PASSWORD'),
        "host": os.getenv('MARIADB_HOST'),
        "port": int(os.getenv('MARIADB_PORT')),
        "database": os.getenv('MARIADB_DATABASE')
    }
    conn= mariadb.connect(**conn_params)
    cur = conn.cursor()
    sql = f"SELECT * FROM movies where year < '{y}'"
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return {"movies": result}

@app.get("/movie")
async def movie(q:str):
    async with httpx.AsyncClient() as client:
        key = os.getenv('API_KEY')
        url = f"https://www.omdbapi.com/?apikey={key}&s={q}&plot=full"
        response = await client.get(url)
        return response.json()
    
@app.get("/movie/item")
async def movie(id:str):
    async with httpx.AsyncClient() as client:
        key = os.getenv('API_KEY')
        url = f"https://www.omdbapi.com/?apikey={key}&i={id}&plot=full"
        response = await client.get(url)
        return response.json()
