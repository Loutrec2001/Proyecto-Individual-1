from fastapi import FastAPI

app = FastAPI()

import pandas as pd
import numpy as np
import ast
import datetime
import warnings
warnings.filterwarnings('ignore')


movies = pd.read_csv('/Users/edwardguzman/Desktop/Laboratorio I/Lab1/movies_dataset.csv')
credits = pd.read_csv('/Users/edwardguzman/Desktop/Laboratorio I/Lab1/credits.csv')

movies['revenue'].fillna(0, inplace=True)
movies['budget'].fillna(0, inplace=True)

credits.drop_duplicates(['id'], inplace = True)
credits['id'] = credits['id'].astype(int, copy=True, errors='raise')
movies.drop_duplicates(['id'], inplace = True)
movies.drop(movies[(movies['id'] == '1997-08-20') | (movies['id'] == '2014-01-01') | (movies['id'] == '2012-09-29')].index, inplace = True)
movies['id'] = movies['id'].astype(int, copy=True, errors='raise')
movies['budget'] = movies['budget'].astype(float, copy=True, errors='raise')

movies = movies.merge(credits, on = 'id')
movies.drop(columns = ['homepage','tagline','video','imdb_id','adult','original_title','poster_path','homepage'], inplace =  True)

def convert(object): # función para desanidar genero y obtener una lista con los generos así como 
    list = []        # Spoken_languaje
    for i in ast.literal_eval(object):
        list.append(i['name'])
    
    return list

def convert_cast(object): #función para desaninar los 5 primeros actores pricipales de las peliculas
    list = []
    counter = 0
    for i in ast.literal_eval(object):
        if counter != 5:
            list.append(i['name'])
            counter += 1
        else:
            break
    
    return list

def convert_direct(object): #Función para desanidar los directores de cada una de las películas
    list = []
    for i in ast.literal_eval(object):
        if i['job'] == 'Director':
            list.append(i['name'])
            break
    
    return list

movies['genres'] = movies['genres'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(convert_direct)
movies.rename(columns={'crew':'Director'}, inplace = True)

movies ['genres'] = movies['genres'].apply(lambda x:[i.replace(' ','') for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(' ','') for i in x])
movies['Director'] = movies['Director'].apply(lambda x:[i.replace(' ','') for i in x])

def str_to_date(time):
    if len(time) < 10:
        return None
    else:
        return datetime.datetime.strptime(time,'%Y-%m-%d')

movies = movies.dropna(subset=['release_date'])
movies['release_date'] = movies['release_date'].apply(str_to_date)
movies['release_year'] = movies['release_date'].dt.year

movies['return'] = round(movies['revenue'] / movies['budget'], 6) #división
movies['return'] = movies['return'].fillna(0) #retornar cero en los nulos
movies.loc[movies['return']==np.inf, 'return'] = 0 #retornar cero en los inf
movies['Director'] = movies['Director'].apply(lambda x: ' '.join(x)) #convertir a String
movies['cast'] = movies['cast'].apply(lambda x: ' '.join(x)) #convertir a String

@app.get("/Cantidad_filmaciones_mes/{Mes}")

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

@app.get("/Cantidad_filmaciones_dia/{Dia}")
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

movies['popularity'] = movies['popularity'].astype(float)

@app.get('/score_titulo/{Titulo}')
def score_title(Titulo):
    a = 0
    Titulo = Titulo.lower()
    for film in movies['title']:
        if film.lower() == Titulo:
            x = movies[['release_date','title','popularity']].loc[movies['title'] == film]
            a += 1 
    
    
    return f'Existen {a} Filmes con el título {Titulo}', x

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

@app.get('/get_actor/{nombre_actor1}')
def get_actor(nombre_actor1):
    nombre_actor = nombre_actor1.replace(' ', '')
    actor_films = movies[movies['cast'].str.contains(nombre_actor, case=False)]['return']
    cant_movies = actor_films.count()
    return_t = actor_films.sum()
    avg_return = return_t / cant_movies

    if cant_movies > 0:
        
        return {'Actor':nombre_actor1, 'cantidad_movies':int(cant_movies), 'retorno_total':int(return_t), 'retorno_promedio':int(avg_return)}

    else:
        return f"No se encontraron registros para el actor {nombre_actor1}"

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

movies['genres'] = movies['genres'].apply(lambda x: ' '.join(x)) 
movies['tags'] =  movies['overview'] + movies['genres'] + ' '+ movies['cast'] + movies['Director']
movies_new = movies[['id', 'title', 'tags']]
movies_new = movies_new.dropna(subset=['tags'])

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
    list1 = []
    for i in text.split():
        list1.append(ps.stem(i))
    
    return " ".join(list1)

movies_new['tags'] = movies_new['tags'].apply(stem)
movies_p = movies_new.head(20000) #selecciono una muestra de 20000

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features= 9000, stop_words='english')
vector = cv.fit_transform(movies_p['tags']).toarray()
cv.get_feature_names_out()

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vector)

@app.get('/recomendacion/{titulo}')
def Recomendacion(titulo:str):
    
    movie_index = movies_p[movies_p['title']  == titulo].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse = True, key = lambda x:x[1])[1:6]
    listM = []
    for i in movie_list:
        
        j = movies_p.iloc[i[0]].title
        listM.append(j)
        
    print('La lista recomendada es: ')
    return listM
    

