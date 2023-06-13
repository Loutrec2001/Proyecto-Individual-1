import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies_p = pd.read_csv('movies_p.csv')

def cosine_similarity_fuction():
    cv = CountVectorizer(max_features= 5000, stop_words='english')
    vector = cv.fit_transform(movies_p['tags']).toarray()
    cv.get_feature_names_out()
    similarity = cosine_similarity(vector)

    return similarity