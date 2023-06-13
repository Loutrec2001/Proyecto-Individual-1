from fastapi import FastAPI
import pandas as pd
import numpy as np
import ast

app = FastAPI()

movies = pd.read_csv('movies_f.csv')


## FUNCIÓN CANTIDAD DE PELÍCULAS POR MES
movies['release_date'] = pd.to_datetime(movies['release_date'])
@app.get("/cantidad_filmaciones_mes/{Mes}")
def cnt_of_films_month(Mes):
    
    months = ["enero", "febrero", "marzo", "abril", "mayo"
          , "junio", "julio", "agosto", "septiembre", 
          "octubre", "noviembre", "diciembre"]

    Mes1 = Mes.lower()
    for j in months:

        if Mes1 == j:
            c = months.index(j) + 1

    a = 0
    for mes in movies['release_date'].dt.month:
        if mes == c:
            a = a+1

    return {'mes':Mes, 'cantidad':a} 


## FUNCIÓN CANTIDAD DE PELÍCULAS POR DIA
@app.get("/cantidad_filmaciones_dia/{Dia}")
def cnt_of_films_day(Dia):

    days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes','sabado','domingo']
    Dia1 = Dia.lower()
    for k in days:
        if k == Dia1:
            c = days.index(k)
    
    b=0
    for day in movies['release_date'].dt.weekday:
        if day == c:
            b = b+1

    return {'dia':Dia, 'cantidad':b} 

## FUNCIÓN SCORE POR TÍTULO
@app.get('/score_titulo/{Titulo}')
def score_title(Titulo):
    a = 0
    Titulo = Titulo.lower()
    for film in movies['title']:
        if film.lower() == Titulo:
            x = movies[['release_date','title','popularity']].loc[movies['title'] == film]
            a += 1 
    
    
    return f'Existen {a} Filmes con el título {Titulo}', x

## FUNCIÓN VOTOS POR TÍTULO
@app.get('/votos_titulo/{Titulo}')
def vote_title(Titulo):
    
    Titulo = Titulo.lower()
    a = 0
    for film in movies['title']:
        if film.lower() == Titulo:
            x = movies[['title','vote_count','vote_average']].loc[movies['title'] == film]
            a = a + 1  

    if a > 1:
        if (x['vote_count'].sum() >= 2000):
            y = x['vote_count'].sum()
            z = x['vote_average'].mean()
            return {'Titulo': Titulo, 'cantidad de films': a, 'voto total': y,'voto promedio': z}
            
        else:
            return 'No es posible hacer el calculo ya que la suma de votos es menor a 2000'
    else:
        if x['vote_count'].values[0] >= 2000:
            y = x['vote_count'].values[0]
            z = x['vote_average'].values[0]
            #return f'La cantidad de votos del filme es de {round(y)} con un promedio de votación de {z}'
            return {'Titulo':Titulo, 'Voto total':y, 'Voto promedio':z}
        else:
            return 'No es posible hacer el calculo ya que la suma de votos es menor a 2000'


## FUNCIÓN ACTOR
movies = movies.dropna(subset=['cast'])
@app.get('/get_actor/{nombre_actor1}')
def get_actor(nombre_actor1):
    nombre_actor = nombre_actor1.replace(' ', '')
    actor_films = movies[movies['cast'].str.contains(nombre_actor, case=False)]['return']
    cant_movies = actor_films.count()
    return_t = actor_films.sum()
    avg_return = return_t / cant_movies
    if cant_movies > 0:
        return {'Actor':str(nombre_actor1), 'cantidad_movies':int(cant_movies), 'retorno_total':int(return_t), 'retorno_promedio':int(avg_return)}
    else:
        return f"No se encontraron registros para el actor {nombre_actor1}."


## FUNCIÓN DIRECTOR
movies = movies.dropna(subset=['Director'])
@app.get('/get_director/{nombre_director1}')
def get_director(nombre_director1):
    nombre_director = nombre_director1.replace(' ', '')
    films_dire = movies[movies['Director'].str.contains(nombre_director, case=False)]
    cant_movies = films_dire.shape[0]

    if cant_movies > 0:
        return_t = films_dire['return'].sum()
        dir_sucess = return_t / cant_movies
        films = films_dire[['title', 'release_date', 'return', 'budget', 'revenue']]
        films = films.reset_index(drop=True)
        
        print(f"El director {nombre_director} ha dirigido {cant_movies} películas. Su éxito a generado un retorno promedio de {dir_sucess:.2f} por pelicula. Las películas dirigidas son:")
        return films
    else:
        return f"No se encontraron registros para el director {nombre_director}."


movies_p = pd.read_csv('movies_p.csv')

# OPERACIONES DE VECTORIZACIÓN
# from sklearn.feature_extraction.text import CountVectorizer
# cv = CountVectorizer(max_features= 5000, stop_words='english')
# vector = cv.fit_transform(movies_p['tags']).toarray()
# cv.get_feature_names_out()
from sklearn.metrics.pairwise import cosine_similarity
# similarity = cosine_similarity(vector)


# @app.get('/recomendacion/{titulo}')
# def movie_recommend(titulo):
#     movie_index = movies_p[movies_p['title']  == titulo].index[0]
#     distances = similarity[movie_index]
#     movie_list = sorted(list(enumerate(distances)),reverse = True, key = lambda x:x[1])[1:6]
#     list_p = []
#     for i in movie_list:
        
#         j = movies_p.iloc[i[0]].title
#         list_p.append(j)
#     return {'lista recomendada': list_p}

from sklearn.feature_extraction.text import TfidfVectorizer


@app.get('/recomendacion/{titulo}')
def recomendacion(titulo):
    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    tfid = vectorizer.fit_transform(movies_p['tags'])
    query = vectorizer.transform([titulo])
    similar = cosine_similarity(query,tfid).flatten()

    ind_simi = np.argpartition(similar, -50)[-50:]
    simil = movies_p.iloc[ind_simi]

    sort_simil = simil.sort_values(by ='popularity', ascending = False)

    popular_simil = sort_simil.head(5)
    resultado_1 = popular_simil['title'].astype(str) 

    return resultado_1



    
    
