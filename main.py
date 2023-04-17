from fastapi import FastAPI
from fastapi.responses import HTMLResponse ,JSONResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd 


#cargando los datos 
movie_df = pd.read_csv("data/data_procesada/movie.csv")
rating=pd.read_csv("./data/ratings/7.csv")
# Cargar los datos
movies_df = pd.read_csv('./data/data_procesada/movie.csv')

# Crear la matriz TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_df['listed_in'])

# Calcular la similitud del coseno
cosine_sim = cosine_similarity(tfidf_matrix)
app = FastAPI()


@app.get('/')
def home():
    return HTMLResponse('<h1 style=color:blue>LA APP JHON </h1>')

@app.get('/get_max_duration/{year}/{platform}/{duration_type}',tags=["movies"])
async def get_max_duration(year:int, platform:str ,duration_type:str):
    #haciendo los respectivos filtros
    df2=movie_df[(movie_df["release_year"]==year) & (movie_df["plataforma"]==platform) & (movie_df["duration_unit"]==duration_type)]
    #halando el el indice del maximo valor
    index_max=df2['duration_int'].idxmax()
    #hallando el nombre de la pelicula
    peli_max=df2.loc[index_max,"title"]
    return {'pelicula':peli_max}

@app.get('/get_score_count/{platform}/{scored}/{year}',tags=["movies"])
async def get_score_count(platform:str, scored:int, year:int):
    df=movie_df[(movie_df["release_year"]==year) & (movie_df["plataforma"]==platform) & (movie_df["score"]>scored)]
    cantidad=df.shape[0]
    return {
        'plataforma': platform,
        'cantidad': cantidad,
        'anio': year,
        'score': scored
    }

@app.get('/get_count_platform/{platform}',tags=["movies"])
async def get_count_platform(platform:str):
    df=movie_df[(movie_df["plataforma"]==platform)]
    count= df.shape[0]
    return {'plataforma': platform, 'peliculas': count}

@app.get('/get_actor/{platform}/{year}',tags=["movies"])
async def get_actor(platform:str, year:int):
    df=movie_df[(movie_df["plataforma"]==platform) & (movie_df["release_year"]==year)]
    actor_masrepetido=df['director'].value_counts().sort_values(ascending=False).idxmax()
    return {
        'plataforma': platform,
        'anio': year,
        'actor': actor_masrepetido,
        'apariciones': actor_masrepetido
    }

@app.get('/prod_per_county/{tipo}/{pais}/{anio}',tags=["movies"])
async def prod_per_county(tipo:str,pais:str,anio:int):
    df=movie_df[(movie_df["country"]==pais) & (movie_df["release_year"]==anio)& (movie_df["type"]==tipo)]
    cant_peliculas_serie=df['duration_unit'].value_counts()

    return {'pais': pais,
             'anio': anio, 
             'peliculas': cant_peliculas_serie[1]
            }

@app.get('/get_contents/{rating}')
async def get_contents(rating:int):
    df=movie_df[movie_df["score"]==10]
    return {'rating': rating, 'contenido': df.shape[0]}

@app.get('/get_recomendation/{title}',tags=["movies"])
async def get_recommendations(title:str):
    idx = movies_df.index[movies_df['title'] == title].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    lista=movies_df['title'].iloc[movie_indices]
    return {'recomendacion':[i for i in lista ]}