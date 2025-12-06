import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

API_KEY = "68284f64569e5bb76e9d651d9fc4d861"

# # Google Drive file id
# file_id = "1vrhoMOCR2vw8kbzYNxkljc3ppW66418S"
# # Construct download URL
# url = f"https://drive.google.com/uc?export=download&id={file_id}"
#
# model_path = "similarity.pkl"
#
# # Download similarity.pkl if not present
# if not os.path.exists(model_path):
#     gdown.download(url, model_path, quiet=False)

file_id = "1vrhoMOCR2vw8kbzYNxkljc3ppW66418S"

model_path = "similarity.pkl"

if not os.path.exists(model_path):
    # This method is the most reliable for large Google Drive files
    gdown.download(id=file_id, output=model_path, quiet=False, use_cookies=False)
    st.write("Files present:", os.listdir())

# Load similarity matrix
with open(model_path, "rb") as f:
    similarity = pickle.load(f)

# Load movies dictionary
with open("movies_dict.pkl", "rb") as f:
    movies_dict = pickle.load(f)

movies = pd.DataFrame(movies_dict)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    poster_path = data.get("poster_path", None)
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


st.title('Movie Recommender System')
selected_movie_name = st.selectbox('List of movies', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(len(names))

    for i in range(len(names)):
        with cols[i]:
            st.image(posters[i], width=150)
            st.write(names[i])
