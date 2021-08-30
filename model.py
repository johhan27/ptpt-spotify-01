from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Song(DB.Model):  # Song to be query
    song_id = DB.Column(DB.Unicode(100), nullable=False, primary_key=True)
    artist_name = DB.Column(DB.String(30))
    track_name = DB.Column(DB.String(100))

    def __repr__(self):
        return '<-- song_id %s -- artist_name %s -- track_name %s -->' % (self.song_id, self.artist_name,
                                                                          self.track_name)


class Track(DB.Model):  # Track = X matched song for another Y song
    track_id = DB.Column(DB.Unicode(100), nullable=False, primary_key=True)
    artist_name = DB.Column(DB.String(30))
    track_name = DB.Column(DB.String(100))

    def __repr__(self):
        return '<-- track_id %s -- artist_name %s -- track_name %s -->' % (self.track_id, self.artist_name,
                                                                           self.track_name)


class Match(DB.Model):
    match_id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    song_id = DB.Column(DB.Unicode(100), DB.ForeignKey("song.song_id"), nullable=False)
    song = DB.relationship('Song', backref=DB.backref('matches'), lazy=True)
    track_id = DB.Column(DB.Unicode(100), DB.ForeignKey("track.track_id"), nullable=False)
    track = DB.relationship('Track', backref=DB.backref("matches"), lazy=True)
    match_score = DB.Column(DB.Integer)

    def __repr__(self):
        return '<-- match_id %s -- song_id %s -- track_id %s -->' % (self.match_id, self.song_id, self.track_id)
