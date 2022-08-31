import pandas as pd

def process_tsv():
    """
    This function processes a tsv file from name.basics.tsv.gz.
    The raw data can be bound here: https://datasets.imdbws.com/
    """
    # importing data from the archive: pandas.read_table takes care
    # of on-the-fly decompression of on-disk data
    data = pd.read_table("./data/name.basics.tsv.gz")

    # selecting only entries where primaryProfession contains actor or actress
    cond1 = data["primaryProfession"].str.contains("actor")
    cond2 = data["primaryProfession"].str.contains("actress")
    data = data[cond1 | cond2]

    # selecting entries with at least two entries in knownForTitle
    # (so that the names.csv is less than 50 MB)
    data["nKnownFor"] = data["knownForTitles"].str.count("tt")
    data = data[data["nKnownFor"] >= 2]

    # renaming columns
    data = data.rename(columns={"nconst":"IMDBID", "primaryName":"Name"})

    # selecting only two columns: IMDBID and Name
    data = data[["IMDBID", "Name"]]
    data = data.dropna()

    # saving dataframe to the file
    data.to_csv("./data/names.csv", index=False)

if __name__ == "__main__":
    process_tsv()