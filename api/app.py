from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

def create_full_movie_df(top_K_movies):
    top_K_MovieLens = top_K_movies.reset_index()
    movies = top_K_MovieLens.merge(ml_25m_movies, on='movieId')[['movieId', 'rating', 'title']].drop_duplicates(subset=['movieId'])
    return movies


def get_number_of_ratings_per_movie():
    counts = ml_25m_ratings.groupby('movieId')['userId'].count().reset_index(name='num_ratings')
    return counts

@app.get("/hello_world")
async def hello_world():
    return {"message" : "Hello, world!"}
