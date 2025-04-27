from flask import Blueprint, render_template, request, redirect, url_for, flash
from Services.spotify_recommendations import get_recommendations
from Services.spotify_oauth import get_spotify_client

recommendations_bp = Blueprint('recommendations', __name__, url_prefix='/recommendations')

# Rotta principale per vedere e ottenere raccomandazioni
@recommendations_bp.route('/', methods=['GET', 'POST'])
def recommendations():
    tracks = []

    if request.method == 'POST':
        # Prendiamo i dati dal form
        seed_artists = request.form.get('seed_artists')
        seed_genres = request.form.get('seed_genres')
        seed_tracks = request.form.get('seed_tracks')
        save_to_playlist = request.form.get('save_to_playlist')

        # Otteniamo le raccomandazioni
        tracks = get_recommendations(seed_artists=seed_artists, seed_tracks=seed_tracks, seed_genres=seed_genres)

        # Se l'utente ha chiesto di salvare la raccomandazione in playlist
        if save_to_playlist == 'yes' and tracks:
            sp = get_spotify_client()

            # Crea una nuova playlist
            user_id = sp.current_user()['id']
            playlist = sp.user_playlist_create(user=user_id, name="Playlist Raccomandazioni", public=False)

            # Aggiunge le tracce consigliate alla nuova playlist
            track_uris = [f"spotify:track:{track['id']}" for track in tracks]
            sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)

            flash('Playlist creata con successo!', 'success')

    # Ritorna la pagina con i brani consigliati
    return render_template('recommendations.html', tracks=tracks)
