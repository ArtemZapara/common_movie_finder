import streamlit as st
import pandas as pd
import imdb

@st.cache(show_spinner=False)
def fetch_data(table):
    df = pd.read_csv(f"./data/{table}.csv")
    return df

@st.cache(show_spinner=False)
def get_person_info(personID):
    person_info = imdb.IMDb().get_person_filmography(personID)
    return person_info

@st.cache(show_spinner=False)
def get_person_filmography(personObject):
    filmography = list()
    keyword = list(set(personObject["data"]["filmography"].keys()) & set(["actor", "actress"]))[0]
    for film in personObject["data"]["filmography"][keyword]:
            filmography.append(film.movieID)
    return filmography

@st.cache(show_spinner=False)
def display_text(person1, person2, length):
    if length == 0:
        text = f"{person1} and {person2} did not star together."
    elif length == 1:
        text = f"{person1} and {person2} starred together in one movie:"
    else:
        text = f"{person1} and {person2} starred together in {length} following movies:"
    return text

@st.cache(show_spinner=False)
def parse_filmography(personObject):
    filmography = dict()
    keyword = list(set(personObject["data"]["filmography"].keys()) & set(["actor", "actress"]))[0]
    for film in personObject["data"]["filmography"][keyword]:
        movieID = film.movieID
        movieData = film.data
        filmography[movieID] = movieData
    return filmography

@st.cache(show_spinner=False)
def process_input(dataframe, text_input):
    df = dataframe[dataframe["Name"].str.contains(text_input, case=False)]
    df = df.sort_values(by=["Name"])
    return df