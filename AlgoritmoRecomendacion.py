import pandas as pd
from math import sqrt 
import numpy as пр
def get_recomendation(title='toy story'):
    movies_df=pd.read_csv("./data/data_procesada/movie.csv")
    rating=pd.read_csv("./data/ratings/7.csv")
    #vamos a crear lista de generos para despues hacer el procesamiento oo
    movies_df['listed_in']=movies_df.listed_in.str.split(',')
    #implemerntacion de las tecnicas one hot
    movies_df_co=movies_df.copy()
    #haciendo el one hot
    for index,row in movies_df.iterrows():
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
    return nfinal


if __name__=="__main__":
    title=input('ingrese el nombre de la pelicula: ') # toy story
    print('*'*50+'\n','la pelicula que le recomendamos son \n')
    a=get_recomendation(title)
    print(a)
