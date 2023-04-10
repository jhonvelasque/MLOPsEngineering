from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

@app.get('/')
def home():
    return HTMLResponse('<h1 style=color:blue> hola mundo </h1>')
@app.get("/inicio")
async def ruta_prueba():
    return "La pagina de jhon"
