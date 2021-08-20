from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from model import Track, Song, Match, DB
from sqlalchemy.exc import IntegrityError
import random
import os  # in case we use Spotify API
from predict import song_choice
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotify.sqlite3'
DB.init_app(app)

df = pd.read_csv("https://raw.githubusercontent.com/brennanashley/DS-Build-3-Spotify/main/spotify_data.csv")

@app.route('/')
def root():
    DB.create_all()
    return render_template('landing.html', matches=Match.query.all())


@app.route('/recommendations')
def recommendations():
    """
    e.g.

    http://127.0.0.1:5000/recommendations?song_id=7fRruZ12gXGwBs0zXQ6e5V
    """
    song_id = request.args['song_id']
    result = song_choice(song_id, df)
    return result


if __name__ == '__main__':
    app.run()
