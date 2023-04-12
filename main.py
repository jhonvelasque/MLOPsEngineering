from fastapi import FastAPI
from fastapi.responses import HTMLResponse ,JSONResponse
import pandas as pd 
app = FastAPI()
#cargando los datos 
movie_df = pd.read_csv("data/data_procesada/movie.csv")

@app.get('/')
def home():
    return HTMLResponse('<h1 style=color:blue>LA APP JHON </h1>')


@app.get("/movie/max",tags=["movies"])
async def get_max_duration(year:int, platform:str ,duration_type:str):
    #haciendo los respectivos filtros
    df2=movie_df[(movie_df["release_year"]==year) & (movie_df["plataforma"]==platform) & (movie_df["duration_unit"]==duration_type)]
    #halando el el indice del maximo valor
    index_max=df2['duration_int'].idxmax()
    #hallando el nombre de la pelicula
    peli_max=df2.loc[index_max,"title"]
    return peli_max

@app.get("/movie/score",tags=["movies"])
async def get_score_count(platform:str, scored:int, year:int):
    df=movie_df[(movie_df["release_year"]==year) & (movie_df["plataforma"]==platform) & (movie_df["score"]>scored)]
    cantidad=df.shape[0]
    return cantidad

@app.get("/movie/platform",tags=["movies"])
async def get_count_platform(platform:str):
    df=movie_df[(movie_df["plataforma"]==platform)]
    return df.shape[0]


@app.get("/movie/actor",tags=["movies"])
async def get_actor(platform:str, year:int):
    df=movie_df[(movie_df["plataforma"]==platform) & (movie_df["release_year"]==year)]
    actor_masrepetido=df['director'].value_counts().sort_values(ascending=False).idxmax()
    return actor_masrepetido

@app.get("/movie/contentent",tags=["movies"])
async def prod_per_county(tipo:str,pais:str,anio:int):
    df=movie_df[(movie_df["country"]==pais) & (movie_df["release_year"]==anio)& (movie_df["type"]==tipo)]
    cant_peliculas_serie=df['duration_unit'].value_counts()
    return(cant_peliculas_serie[1],cant_peliculas_serie[0])

@app.get("/movie/contents",tags=["movies"])
async def get_contents(rating:int):
    df=movie_df[movie_df["score"]==10]
    return df.shape[0]
#postgres://movie_m8dy_user:WMCe34LEJp5xWHMBqw85EAjqm5wEgxdL@dpg-cgqabgseooggt0vd6d20-a.oregon-postgres.render.com/movie_m8dy