import streamlit as st
import pickle
import pandas as pd
import requests


movies = pd.read_pickle("movies.pkl")
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))
api_key = "c43bd02cd71162d975655d5d1cac7722"

def fetch_image(movie_id) :
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, api_key))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    mov_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies_images = list()
    recommended_movies = list()
    for i in mov_list:
        recommended_movies_images.append(fetch_image(movies.iloc[i[0]].id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_images


st.title('Movie Recommender System')

#https://api.themoviedb.org/3/movie/65?api_key=c43bd02cd71162d975655d5d1cac7722&language=en-US

movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies_list)

if st.button('Recommend'):
    names, images = recommend(movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write(names[0])
        st.image(images[0])

    with col2:
        st.write(names[1])
        st.image(images[1])

    with col3:
        st.write(names[2])
        st.image(images[2])

    with col4:
        st.write(names[3])
        st.image(images[3])

    with col5:
        st.write(names[4])
        st.image(images[4])
