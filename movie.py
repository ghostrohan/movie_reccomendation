import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np



similarity = pickle.load(open('similarity.pkl','rb'))
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
id_list = pickle.load(open('id_list.pkl','rb'))
movies = pd.DataFrame(movies_dict)



def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ebe1f2f3d5c9ccf61dd734363d4f8e37&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path']

def fetch_decription(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ebe1f2f3d5c9ccf61dd734363d4f8e37&language=en-US'.format(movie_id))
    data = response.json()
    return data['overview']

def fetch_trailer(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}/videos?api_key=ebe1f2f3d5c9ccf61dd734363d4f8e37&language=en-US".format(movie_id))
    data = response.json()
    if len(data['results'])>0:
        return "https://www.youtube.com/watch?v=" + data['results'][0]['key']
    return ''
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    new_list = []
    recommended_movie_poster = []
    movie_overview = []
    youtube_list = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        #fetch poster from API
        new_list.append((movies.iloc[i[0]].title))
        recommended_movie_poster.append(fetch_poster(movie_id))
        movie_overview.append(fetch_decription(movie_id))
        youtube_list.append(fetch_trailer(movie_id))
    return new_list,recommended_movie_poster,movie_overview,youtube_list


st.title('Movie Recommendation System')
if st.button("Pick me a Movie"):
    selected_movie_name = movies.sample()['title'].values[0]
    recc, poster, overview, youtube_link = recommend(selected_movie_name)
    i = 0
    while i < 5:
        st.header(recc[i])
        st.image(poster[i],width=500)
        st.write(overview[i])
        st.write("Youtube Trailer")
        st.video(youtube_link[i])
        i = i + 1


selected_movie_name = st.selectbox('Enter Movies',movies['title'].values)

if st.button('Recommend'):
    recc,poster,overview,youtube_link = recommend(selected_movie_name)
    i = 0
    while i < 5:
        st.header(recc[i])
        st.image(poster[i],width=500)
        st.write(overview[i])
        st.write("Youtube Trailer")
        st.video(youtube_link[i])
        i = i + 1

