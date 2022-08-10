from re import I
import pandas as pd

data = pd.read_csv("./data/Top 1000 Actors and Actresses.csv")

data["IMDBID"] = data["Const"]

actors_1000 = data[["IMDBID", "Name"]]
actors_1000.to_csv("./data/actors_1000.csv", index=False)