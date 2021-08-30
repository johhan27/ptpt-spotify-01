from model import DB, Song, Track
import pandas as pd
import numpy as np
import sqlite3


def upsert_songs(df):
    df_last_song_id = df['track_id'].iloc[-1]
    if Song.query.get(df_last_song_id): # if it's up to date
        DB.session.commit()
    else:
        con = sqlite3.connect('spotify.sqlite3')
        cur = con.cursor()

        db_last_row = cur.execute('select * from song order by song_id desc limit 1').fetchone()
        cur.close()
        con.close()
        if db_last_row is None:
            cut_df = df
        else:
            last_stored_id = db_last_row[0]
            df_cutoff_index = df.index[df['track_id'] == last_stored_id].tolist()
            cut_df = df.iloc[df_cutoff_index[0]:]
        for index, row in cut_df.iterrows():
            db_song = Song(song_id=row['track_id'], artist_name=row['artist_name'], track_name=row['track_name'])
            db_track = Track(track_id=row['track_id'], artist_name=row['artist_name'], track_name=row['track_name'])
            DB.session.add(db_song)
            DB.session.add(db_track)
        DB.session.commit()
