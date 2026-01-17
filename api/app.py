from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from google.cloud import bigquery
import pandas as pd
import io

client = bigquery.Client()
app = FastAPI()


def query_df(query, client):
    query_job = client.query(query)
    df = query_job.result().to_dataframe()

    return df

# Create our dataframes from our BigQuery data warehouse
ml_25m_movies_query = "SELECT * FROM `mlops-movie-recommender.ml_25m.movies`;"
ml_25m_movies = query_df(ml_25m_movies_query, client)

ml_25m_ratings_query = "SELECT * FROM `mlops-movie-recommender.ml_25m.ratings`;"
ml_25m_ratings = query_df(ml_25m_ratings_query, client)

big_tmdb_overview_query = "SELECT * FROM `mlops-movie-recommender.big_tmdb.overview`;"
big_tmdb_overview = query_df(big_tmdb_overview_query, client)

big_tmdb_keywords_query = "SELECT * FROM `mlops-movie-recommender.big_tmdb.keywords`;"
big_tmdb_keywords = query_df(big_tmdb_keywords_query, client)


# Recommendation models
def create_full_movie_df(top_K_movies):
    top_K_MovieLens = top_K_movies.reset_index()
    movies = top_K_MovieLens.merge(ml_25m_movies, on='movieId')[['movieId', 'rating', 'title']].drop_duplicates(subset=['movieId'])
    return movies


def get_number_of_ratings_per_movie():
    counts = ml_25m_ratings.groupby('movieId')['userId'].count().reset_index(name='num_ratings')
    return counts


# API functions
@app.get("/hello_world")
async def hello_world():
    return {"message" : "Hello, world!"}
