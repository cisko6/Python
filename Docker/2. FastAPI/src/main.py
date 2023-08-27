import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_name():
    return {"Username": "cisko6"}

@app.get("/nginx")
def get_nginx():
    str = "Welcome to nginx!"
    return str

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
