import streamlit as st
import pandas as pd
import imdb
from helpers import *

ia = imdb.IMDb()
st.set_page_config(layout="wide")

names = fetch_data("names")

col1, _, col2, _, col3 = st.columns([1,1,2,1,1])
with col1:
    input1 = st.text_input(label="Please provide a hint and then select a star in the list below", key="input1")
    if len(input1) >= 3:
        df_input1 = process_input(names, input1)
        if df_input1.empty:
            st.write("No in the database")
        else:
            select1 = st.selectbox(
                "",
                df_input1["Name"],
                key="1"
            )
            code1 = names[names["Name"] == select1]["IMDBID"].values[0]
            id1 = code1[2:]
            person1 = get_person_info(id1)
            filmography1 = parse_filmography(person1)
            if "headshot" in person1["data"].keys():
                person1ImageURL = person1["data"]["headshot"]
                st.image(person1ImageURL)
            else:
                st.write("No photo")

with col3:
    input2 = st.text_input(label="Please provide a hint and then select a star in the list below", key="input2")
    if len(input2) >= 3:
        df_input2 = process_input(names, input2)
        if df_input2.empty:
            st.write("No results in the database")
        else:
            select2 = st.selectbox(
                "",
                df_input2["Name"],
                key="2"
            )
            code2 = names[names["Name"] == select2]["IMDBID"].values[0]
            id2 = code2[2:]
            person2 = get_person_info(id2)
            filmography2 = parse_filmography(person2)
            if "headshot" in person2["data"].keys():
                person2ImageURL = person2["data"]["headshot"]
                st.image(person2ImageURL)
            else:
                st.write("No photo")

with col2:
    if st.button("Find the common filmography"):
        if id1 != id2:
            commonMovieIDs = set(filmography1).intersection(set(filmography2))

            text = display_text(select1, select2, len(commonMovieIDs))
            st.write(text)

            if len(commonMovieIDs) > 0:
                commonMovies = dict()
                for movieID in commonMovieIDs:
                    movie = filmography1[movieID]
                    commonMovies[movieID] = movie

                commonMovies = dict(sorted(commonMovies.items(), key=lambda item: item[1]["year"]))
                for movieID, movie in commonMovies.items():
                    movieData = ia.get_movie(movieID)
                    coverURL = movieData.get_fullsizeURL()
                    caption = f"{movie['title']} ({movie['year']})"
                    st.image(coverURL, caption=caption, use_column_width=True)