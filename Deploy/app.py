import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=cb6f6b1a87681562ef8592292e9e3d13&language=en-US')
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except KeyError:
        return None
    except Exception as e:
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        recommended_movies_posters.append(poster_url if poster_url else 'default_poster_url.jpg')

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('How would you like to?', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
      
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"<h3 style='text-align: center; font-size:16px;'>{names[0]}</h3>", unsafe_allow_html=True)
        st.image(posters[0])
    with col2:
        st.markdown(f"<h3 style='text-align: center; font-size:16px;'>{names[1]}</h3>", unsafe_allow_html=True)
        st.image(posters[1])
    with col3:
        st.markdown(f"<h3 style='text-align: center; font-size:16px;'>{names[2]}</h3>", unsafe_allow_html=True)
        st.image(posters[2])
    with col4:
        st.markdown(f"<h3 style='text-align: center; font-size:16px;'>{names[3]}</h3>", unsafe_allow_html=True)
        st.image(posters[3])
    with col5:
        st.markdown(f"<h3 style='text-align: center; font-size:16px;'>{names[4]}</h3>", unsafe_allow_html=True)
        st.image(posters[4])
