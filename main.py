from fastapi import FastAPI
from fastapi.responses import HTMLResponse ,JSONResponse
import pandas as pd 


#cargando los datos 
movie_df = pd.read_csv("data/data_procesada/movie.csv")
rating=pd.read_csv("./data/ratings/7.csv")
app = FastAPI()


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
@app.get('/get_recomendation/{title}',tags=["movies"])
async def get_recomendation(title):
    #vamos a crear lista de generos para despues hacer el procesamiento oo
    movie_df = pd.read_csv("data/data_procesada/movie.csv")
    rating=pd.read_csv("./data/ratings/7.csv")
    movie_df['listed_in']=movie_df.listed_in.str.split(',')
    #implemerntacion de las tecnicas one hot
    movies_df_co=movie_df.copy()
    #haciendo el one hot
    for index,row in movie_df.iterrows():
        for genre in row['listed_in']:
            movies_df_co.at[index,genre.strip()]=1
    #asignamos un cero a als peliculas que no corresponden 
    movies_df_co.fillna(0,inplace=True)

    #eliminando las columnas que no necesitamos
    rating=rating.drop(columns='timestamp')
    #haciendo el perfil del usuario
    #entrada 
    usuario=[
        {'title':title,'rating':5},  
    ]
    entrada_peli=pd.DataFrame(usuario)
    # primero vemos si las peliculass del ususario estan en nuestro data set
    movies_df_co.rename(columns={'id':'movieId'},inplace=True)
    index=movies_df_co[movies_df_co['title'].isin(entrada_peli['title'].str.strip()).tolist()]
    index['movieId']=index['movieId'].str.strip()
    entrada_peli=entrada_peli.merge(index,on='title',how='outer')
    entrada_peli=entrada_peli.iloc[:, [0,1,12] + list(range(17, len(movies_df_co.columns)))]
    #utilizamos una matriz. qu sepraliza con la funcion DOC
    #resetiamos el indice
    entrada_peli.reset_index(drop=True,inplace=True)
    #creando la tabla de generos del perefil del usuario
    tabla_generos=entrada_peli.iloc[:,3:]
    perfil_usuario=tabla_generos.transpose().dot(entrada_peli['rating_x'])
    #categorias que prefiere el ussuario
    perfil_usuario
    generos=movies_df_co.set_index(movies_df_co['movieId'])
    generos=generos.iloc[:,16:]
    #creaando el promedio ponderado para recomendar nuestra peliculas
    recom=((generos*perfil_usuario).sum(axis=1))/(perfil_usuario.sum())
    recom=recom.sort_values(ascending=False)
    final=movies_df_co.loc[movies_df_co['movieId'].isin(recom.head(5).keys())]
    nfinal=final[['title']]
    return {'recomendacion':get_recomendation(nfinal)}
#postgres://movie_m8dy_user:WMCe34LEJp5xWHMBqw85EAjqm5wEgxdL@dpg-cgqabgseooggt0vd6d20-a.oregon-postgres.render.com/movie_m8dy