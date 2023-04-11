from fastapi import FastAPI
from fastapi.responses import HTMLResponse ,JSONResponse
import pandas as pd 
app = FastAPI()
#cargando los datos 
movie_df = pd.read_csv("data/data_procesada/movie.csv")

@app.get('/')
def home():
    return HTMLResponse('<h1 style=color:blue>AMOVIES JHON </h1>')
""" 
Película (sólo película, no serie, ni documentales, etc) con mayor duración según año,
plataforma y tipo de duración. La función debe llamarse get_max_duration(year, platform,
duration_type) y debe devolver sólo el string del nombre de la película. """

@app.get("/movies")
async def ruta_pruebaget_max_duration():
    movies=movie_df.head()
    return f'{movies}'
   
#postgres://movie_m8dy_user:WMCe34LEJp5xWHMBqw85EAjqm5wEgxdL@dpg-cgqabgseooggt0vd6d20-a.oregon-postgres.render.com/movie_m8dy