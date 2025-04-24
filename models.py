from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modello utente
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    playlists = db.relationship('Playlist', backref='user', lazy=True)  # Relazione con le playlist

class Playlist(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=True)
    url = db.Column(db.String, nullable=False, default="https://open.spotify.com")  # Valore predefinito
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Associa la playlist a un utente


