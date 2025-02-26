from flask import Blueprint, render_template, redirect, url_for, session
from Services.spotify_oauth import get_spotify_object
import spotipy

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    token_info = session.get('token_info')
    if token_info:  
        spotify = get_spotify_object(token_info)
        sp = get_spotify_object(token_info) 
        user_info = sp.current_user()
        print(user_info)
        playlists = sp.current_user_playlists()['items']
        return render_template('home.html', user_info=user_info, playlists=playlists)
    else:
        return render_template('home.html', user_info=None)


@home_bp.route('/playlist/<playlist_id>')
def brani(playlist_id):
    token_info = session.get('token_info')
    if not token_info:
        return redirect(url_for('auth.login'))

    sp = get_spotify_object(token_info)
    playlist = sp.playlist(playlist_id)
    
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    
    return render_template('playlist.html', playlist=playlist, tracks=tracks)

@home_bp.route('/artisti')
def top_artists():
    token_info = session.get('token_info')
    if not token_info:
        return redirect(url_for('auth.login'))

    sp = get_spotify_object(token_info)
    artists = []
    
    # Controlla che sp sia definito
    if sp is None:
        return "Errore: Spotipy non è stato inizializzato correttamente", 500

    # Cerca i 50 artisti più popolari
    results = sp.search(q='year:2025', type='artist', limit=50)

    for artist in results['artists']['items']:
        name = artist['name']
        image = artist['images'][0]['url'] if artist['images'] else ""
        popularity = artist['popularity']

        artists.append({'name': name, 'image': image, 'popularity': popularity})

    # Ordina per popolarità
    artists = sorted(artists, key=lambda x: x['popularity'], reverse=True)

    return render_template('artisti.html', artists=artists)