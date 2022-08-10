import streamlit as st
import pandas as pd
import imdb
from helpers import *

ia = imdb.IMDb()
st.set_page_config(layout="wide")

actors = fetch_data("actors_1000")

col1, _, col2, _, col3 = st.columns([1,1,2,1,1])
with col1:
    select1 = st.selectbox(
        "Select star",
        actors["Name"],
        key="1"
    )
    code1 = actors[actors["Name"] == select1]["IMDBID"].values[0]
    id1 = code1[2:]
    person1 = get_person_info(id1)
    person1ImageURL = person1["data"]["headshot"]
    st.image(person1ImageURL)

    movieIDs1 = get_person_filmography(person1)

with col3:
    select2 = st.selectbox(
        "Select star",
        actors["Name"],
        key="2"
    )
    code2 = actors[actors["Name"] == select2]["IMDBID"].values[0]
    id2 = code2[2:]
    person2 = get_person_info(id2)
    person2ImageURL = person2["data"]["headshot"]
    st.image(person2ImageURL)

    movieIDs2 = get_person_filmography(person2)

with col2:
    if st.button("Find the common filmography"):
        if id1 != id2:
            commonMovieIDs = list(set(movieIDs1) & set(movieIDs2))
            text = display_text(select1, select2, len(commonMovieIDs))
            st.write(text)

            if len(commonMovieIDs) > 0:
                commonMovies = dict()
                for id in commonMovieIDs:
                    movie = ia.get_movie(id)
                    field = dict()
                    field["title"] = movie.data["original title"]
                    field["year"] = movie.data["year"]
                    commonMovies[id] = field

                commonMovies = dict(sorted(commonMovies.items(), key=lambda item: item[1]["year"]))
                for movie in commonMovies.values():
                    title = f"{movie['title']} ({movie['year']})"
                    st.write(title)