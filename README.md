# Proyecto-Individual-Sistema de recomendación.

Se realiza en este proyecto un sistema de recomendación y consulta para una base de Datos de Películas.

Base de Datos Movies: https://drive.google.com/file/d/1Q4dhHb3XT_30f3wog4dooBwfK9R5S5UI/view?usp=sharing

Base de Datos Credits: https://drive.google.com/file/d/1JKwLt-QHAZOI1ScInkcyAL5vRjgijUkQ/view?usp=sharing


la base Movies contiene los siguientes datos:

![Diccionario de Datos]https://github.com/Loutrec2001/Proyecto-Individual-1/blob/main/Screen%20Shot%202023-06-11%20at%2011.27.33%20PM.png

 
## Carga y Transformación de Datos.

Se realizan eliminación de duplicados, eliminación de nulos en ciertas columnas y eliminación de columnas no necesarias para el estudio; esto es:

Columnas:

1. 'homepage'
2. 'tagline'
3. 'video'
4. 'imdb_id'
5. 'adult'
6. 'original_title'
7. 'poster_path'
8. 'homepage'

## Desanidar datos

Los datos de las varias columnas se encuentran anidados por ende, se desanidan los necesarios para las consultas. Por ende, se desanidan los datos de Genres, Cast y Crew.

- Para Cast(Elenco) tomamos los primeros 5 nombre de los actores de cada película, ya que, no se quere tener en cuenta actores que sean extras o actores secundarios.
- Para Crew(Equipo de Producción) tomamos tan solo el nombre del director de cada película.

Por último se relacionan las dos bases de datos a través del id y aplicando la función merge.

## Funciones

Se contruyen 6 funciones de consulta:

1. Cantidad de Filmaciones Mes.
2. Cantidad de Filmaciones Día.
3. Puntuación de Película según Título.
4. Cantidad y promedio de votos de Película según Título.
5. Retorno, promedio de retorno y cantidad de películas de actor.
6. Costo, ganancia retorno y cantidad de películas de director.

## Sistema de recomendación

Para generar el sistema de recomendación nos basamos en el resumen de cada película, los actores, el genero de clasificación de las películas y el director. 

Pero en primera instancia realizamos un análisis estadístico de la variable popularidad para ver si tomamos todos los registros. o para optimizar tomamos los registros con mayor popularidad.

Generamos un corto análisis de los límites para que sean atípicos y filtramos las base original (nos quedamos con aproximadamente 20000) registros.

Creamos la variable etiqueta:
movies['tags'] =  movies['overview'] + movies['genres'] + ' '+ movies['cast'] + movies['Director']


Esta variable es de tipo String y contiene la información más relevante para crear la vectorización.

Se aplica la vectorización con CountVectorizer de Sklearn y luego aplicamos cosine_similarity para buscar la matriz de valores de similitud entre cada texto para de este modo recomendar a traves de la vectorización.

Por último realizamos dos funciones de recomendación:

1. A través unicamente de elementos similares o comunes (genero, resumen, actores y director)
2. Tomando todos los 45 mil registros y realizando de nuevo un analisis de elementos similares pero agregando la popularidad como un elemento más para que recomendara a través de la popularidad.

Por último, utilizamos FastApi: /Users/edwardguzman/Documents/Documentos/Primer-Laboratorio/Screen Shot 2023-06-12 at 3.49.46 AM.png

Nota: No se coloca la segunda función es FastApi para no generar confusión en las funciones programadas.

## Fast Api y Deploy en Render

Ya que se tiene todas las funciones probadas se realiza la ejecución en FastApi. Se realiza el Deploy en Render, el web service centa con la dirección:

https://prueba-i4mb.onrender.com/docs

## Link del video  

https://youtu.be/Kr3YfWPvNpI