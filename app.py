import streamlit as st
import pandas as pd
import imdb
from helpers import *

ia = imdb.IMDb()
st.set_page_config(layout="wide")

names = fetch_data("names")

with st.container():
    _, column, _ = st.columns([1,2,1])
    with column:
        btn = st.button("Find the common filmography")

with st.container():
    _, clm, _ = st.columns([1,2,1])
    with clm:
        placeholder = st.empty()

# col1, _, col2, _, col3 = st.columns([1,1,1,1,1])
cols = st.columns([1,1,1,1])

with cols[0]:
    input1 = st.text_input(label="Please provide a hint and then select a star in the list below", key="input1")
    if len(input1) >= 3:
        df_input1 = process_input(names, input1)
        if df_input1.empty:
            st.write("This name is not found in the database")
        else:
            select1 = st.selectbox(
                "",
                df_input1["Name"],
                key="1"
            )
            id1, filmography1, image1 = parse_selection(df_input1, select1)
            st.image(image1)

with cols[3]:
    input2 = st.text_input(label="Please provide a hint and then select a star in the list below", key="input2")
    if len(input2) >= 3:
        df_input2 = process_input(names, input2)
        if df_input2.empty:
            st.write("This name is not found in the database")
        else:
            select2 = st.selectbox(
                "",
                df_input2["Name"],
                key="2"
            )
            id2, filmography2, image2 = parse_selection(df_input2, select2)
            st.image(image2)

if btn:
    if "id1" not in locals() or "id2" not in locals():
        placeholder.warning("Make sure you selected two stars!")
    elif id1 != id2:
        commonMovieIDs = set(filmography1).intersection(set(filmography2))

        text = display_text(select1, select2, len(commonMovieIDs))
        placeholder.write(text)

        if len(commonMovieIDs) > 0:
            commonMovies = dict()
            for movieID in commonMovieIDs:
                movie = filmography1[movieID]
                commonMovies[movieID] = movie

            idx = 0
            commonMovieIDs = list(commonMovieIDs)
            while idx < len(commonMovieIDs):
                for _ in range(len(commonMovieIDs)):
                    for col_num in range(1,3):
                        if idx < len(commonMovieIDs):
                            movieID = commonMovieIDs[idx]
                            movieData = ia.get_movie(movieID)
                            coverURL = movieData.get_fullsizeURL()
                            caption = movieData["title"]
                            cols[col_num].image(coverURL, caption=caption, use_column_width=True)
                            idx+=1