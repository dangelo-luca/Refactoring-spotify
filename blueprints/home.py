from flask import Blueprint, render_template, redirect, url_for, session
from Services.spotify_oauth import get_spotify_object
import spotipy

home_bp = Blueprint('home', __name__)
@home_bp.route('/home')
def home():
    token_info = session.get('token_info') #recupero token sissione (salvato prima)
    if not token_info:
        return redirect(url_for('auth.login'))
    sp = get_spotify_object(token_info) #usiamo il token per ottenere i dati del profilo
    user_info = sp.current_user()
    print(user_info) #capiamo la struttura di user_info per usarle nel frontend
    playlists = sp.current_user_playlists()['items'] #sempre tramite il token sp preso prima
    return render_template('home.html', user_info=user_info, playlists=playlists) #passo le info utente all'home.html

@home_bp.route('/playlist/<playlist_id>')
def brani(playlist_id):
    token_info = session.get('token_info')
    if not token_info:
        return redirect(url_for('auth.login'))

    sp = get_spotify_object(token_info)
    playlist = sp.playlist(playlist_id)
    
    results = sp.playlist_items(playlist_id)
    tracks = results['items']  # Lista di canzoni
    
    # Pagina di ritorno
    return render_template('playlist.html', playlist=playlist, tracks=tracks)
