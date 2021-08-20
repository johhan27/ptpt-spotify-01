from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np


def song_choice(song_id, df):
    """
    Let us help you find new songs using our nearest neighbors model!
    """
    # columns to drop for fitting
    c = ["duration_ms", "index", "genre", "artist_name", "track_id", "track_name", "key", "mode"]
    # get song from user input
    song = df[df["track_id"] == song_id].iloc[0]
    df_selected = df.copy()
    if not pd.isnull(song["genre"]):  # If genre, set subset to only genre
        df_selected = df[df["genre"] == song["genre"]]
    # nearest neighbors
    nn = NearestNeighbors(n_neighbors=11, algorithm="kd_tree")
    nn.fit(df_selected.drop(columns=c))
    song = song.drop(index=c)
    song = np.array(song).reshape(1, -1)
    new = df_selected.iloc[nn.kneighbors(song)[1][0][1:11]]
    # return artist name, track id, and track name
    new2 = new[['artist_name', 'track_id', 'track_name']].copy()
    return new2.to_json(orient="records")
