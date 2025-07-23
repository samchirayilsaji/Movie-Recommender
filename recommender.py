import pandas as pd
import ast

movies = pd.read_csv("https://drive.google.com/uc?id=1LBY4h6SrBTAcwvY-YU-CdnYSkrvsmFBQ")
credits = pd.read_csv("https://drive.google.com/uc?id=1Y-uBP79WYcymKUz0vv9aqIRpQ3XvbFgl")


df = pd.merge(movies, credits, on="title")
print(df.columns)
print(df[['title','genres','cast','crew']].head())

def extract_names(obj_str, key='name', limit=3):
    try:
        items = ast.literal_eval(obj_str)
        return [item.get(key,'') for item in items[:limit]]
    except(ValueError, SyntaxError):
        return []
    
df['cast_names'] = df['cast'].apply(lambda x: extract_names(x))
print(df[['title', 'cast_names']].head().to_string(index=False))

def extract_genres(obj_str):
    try:
        items = ast.literal_eval(obj_str)
        return [item.get('name', '')for item in items]
    except(ValueError, SyntaxError):
        return []
    
def extract_director(obj_str):
    try:
        items = ast.literal_eval(obj_str)
        for item in items:
            if item.get('job') == 'Director':
                return item.get('name', '')
        return ''
    except(ValueError, SyntaxError):
        return ''

df['director'] = df['crew'].apply(extract_director)

df['genre_names'] = df['genres'].apply(extract_genres)
print("\n Genre Tags:")
print(df[['title', 'genre_names']].head().to_string(index=False))

df['genres_str'] = df['genre_names'].apply(lambda x: ' '.join(x))
df['cast_str'] = df['cast_names'].apply(lambda x: ' '.join(x))

df['overview'] = df['overview'].fillna('').astype(str)

df['tags'] = df['overview'] + ' ' + df['genres_str'] + ' ' + df['cast_str'] + ' ' + df['director']
df['tags'] = df['tags'].str.lower() 

print("\nCombined Tags:")
print(df[['title', 'tags']].head(3).to_string(index=False))


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

cv= CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df['tags']).toarray()
similarity= cosine_similarity(vectors)


def recommend(movie_title):
    movie_title = movie_title.lower().strip()
    if movie_title not in df['title'].str.lower().values:
        return []

    idx = df[df['title'].str.lower() == movie_title].index[0]
    input_genres = set(df.loc[idx, 'genre_names'])

    distances = list(enumerate(similarity[idx]))
    similar_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:]

    top_movies = []
    seen_titles = set()

    for i in similar_movies:
        movie = df.iloc[i[0]]
        title = movie['title']
        movie_genres = set(movie['genre_names'])

        if (
            title not in seen_titles
            and movie_genres & input_genres
            and movie['vote_count'] > 500
            and movie['vote_average'] >= 6.5
        ):
            poster_path = movie.get('poster_path', '')
            top_movies.append((title, movie['vote_average'], poster_path))
            seen_titles.add(title)

        if len(top_movies) == 10:
            break

    return top_movies

