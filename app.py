import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=165138f35edd5c9fe366316a8b815e19&language=en-US')
    data = response.json()
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_poster

# Load data


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-image: url(background_img.jpg);
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Arial', sans-serif;
    }
    .title {
        text-align: center;
        color: #FF6347;
        font-size: 48px;
        font-weight: bold;
        margin-top: 20px;
    }
    .subtitle {
        text-align: center;
        color: #4682B4;
        font-size: 24px;
        margin-bottom: 20px;
    }
    .recommend-button {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .poster-container {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 10px;
        border-radius: 10px;
        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);
        margin: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .poster-container img {
        border-radius: 10px;
        width: 100%;
        max-width: 300px;
    }
    .poster-title {
        color: white;
        margin-top: 10px;
        font-size: 18px;
        text-align: center;
    }
    .footer {
        text-align: center;
        color: #2F4F4F;
        font-size: 18px;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app
st.markdown('<h1 class="title">Movie Recommender System</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="subtitle">Find your next favorite movie</h3>', unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend', key='recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(f'''
                <div class="poster-container">
                    <img src="{poster}" alt="{name}">
                    <div class="poster-title">{name}</div>
                </div>
            ''', unsafe_allow_html=True)

st.markdown('<p class="footer">Made with ❤️ by Shravani Ghongde</p>', unsafe_allow_html=True)
