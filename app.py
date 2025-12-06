import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = "68284f64569e5bb76e9d651d9fc4d861"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # some movies may not have poster_path
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
        movie_id = movies.iloc[i[0]].movie_id   # make sure dataset contains movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie recommender system')
selected_movie_name = st.selectbox('List of movies', (movies['title'].values))

# if st.button('Recommend'):
#     names, posters = recommend(selected_movie_name)
#     for i in range(len(names)):
#         st.image(posters[i], width=150)   # smaller poster size
#         st.write(names[i])

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(len(names))   # create 5 columns side by side

    for i in range(len(names)):
        with cols[i]:
            st.image(posters[i], width=150)
            st.write(names[i])

