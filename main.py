from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import psycopg2
app = FastAPI()

conexion = psycopg2.connect(
   host='dpg-cgqabgseooggt0vd6d20-a.oregon-postgres.render.com',
   user='movie_m8dy_user',
   password='WMCe34LEJp5xWHMBqw85EAjqm5wEgxdL',
   dbname='movie_m8dy'   
)

@app.get('/')
def home():
    return HTMLResponse('<h1 style=color:blue>AMOVIES JHON </h1>')
""" 
Película (sólo película, no serie, ni documentales, etc) con mayor duración según año,
plataforma y tipo de duración. La función debe llamarse get_max_duration(year, platform,
duration_type) y debe devolver sólo el string del nombre de la película. """
@app.get("/movie")
async def ruta_prueba():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM alumno")
    lista=[]
    for fila in cursor:
        lista.append(fila)
    conexion.close()
    return lista
#postgres://movie_m8dy_user:WMCe34LEJp5xWHMBqw85EAjqm5wEgxdL@dpg-cgqabgseooggt0vd6d20-a.oregon-postgres.render.com/movie_m8dy