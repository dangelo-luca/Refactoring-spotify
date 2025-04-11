from flask import Blueprint, render_template, redirect, url_for, session,request,flash
from Services.spotify_oauth import get_spotify_object , get_spotify_client
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from models import db, Playlist
from flask_login import login_required, current_user
from Services.num import analyze_and_visualize
home_bp = Blueprint('home', __name__)




@home_bp.route("/home", methods=["GET", "POST"])
@login_required
def home():
    sp = get_spotify_client()
    user_info, playlists = None, []
    if session.get("token_info"):
        try:
            user_info = sp.current_user()
            playlists = sp.current_user_playlists()["items"]
        except Exception:
            pass  
    search_results = []
    query = ""

    if request.method == "POST":
        # Controlla se è una richiesta per aggiungere una playlist ai preferiti
        if "playlist_id" in request.form:
            playlist_id = request.form.get("playlist_id")
            playlist_name = request.form.get("playlist_name")
            playlist_owner = request.form.get("playlist_owner")
            playlist_image = request.form.get("playlist_image")
            # Salva solo la playlist selezionata nel database per l'utente autenticato
            if not Playlist.query.filter_by(id=playlist_id, user_id=current_user.id).first():  # Evita duplicati per utente
                new_playlist = Playlist(
                    id=playlist_id,
                    name=playlist_name,
                    owner=playlist_owner,
                    image=playlist_image,
                    user_id=current_user.id  # Associa la playlist all'utente autenticato
                )
                db.session.add(new_playlist)
                db.session.commit()
        # Controlla se è una ricerca
        elif "query" in request.form:
            query = request.form.get("query", "").strip()
            if query:
                try:
                    results = sp.search(q=query, type="playlist", limit=50)
                    search_results = [
                        {
                            "id": playlist["id"],
                            "name": playlist.get("name", "Senza Nome"),
                            "owner": playlist["owner"].get("display_name", "Sconosciuto"),
                            "image": playlist["images"][0]["url"] if playlist.get("images") else None
                        }
                        for playlist in results.get("playlists", {}).get("items", [])
                        if playlist
                    ]
                except Exception as e:
                    print("Errore nella ricerca:", e)

    # Recupera le playlist salvate dal database per l'utente autenticato
    saved_playlists = Playlist.query.filter_by(user_id=current_user.id).all()

    if len(session['selected_playlists']) == 2:
        session['selected_playlists'] = []
        flash("Selezione delle playlist resettata.")

        
    return render_template(
        "home.html",
        user_info=user_info,
        playlists=playlists,
        query=query,
        search_results=search_results,
        saved_playlists=saved_playlists
    )

@home_bp.route("/playlist/<playlist_id>")
def playlist(playlist_id):
    sp = get_spotify_client() 
    playlist_data, tracks = None, []
    try:
        playlist_data = sp.playlist(playlist_id)
        tracks_data = playlist_data["tracks"]["items"]

        tracks = [
            {
                "name": track["track"].get("name", "Senza Nome"),
                "artist": track["track"]["artists"][0].get("name", "Sconosciuto"),
                "album": track["track"]["album"].get("name", "Senza Nome"),
                "cover": track["track"]["album"].get("images", [{}])[0].get("url", None)
            }
            for track in tracks_data if track.get("track")
        ]
    except Exception as e:
        print("Errore nel recupero della playlist:", e)
    user_info = sp.current_user()
    charts = analyze_and_visualize(playlist_id)

    return render_template("playlist.html", user_info=user_info, playlist=playlist_data, tracks=tracks, charts=charts)

@home_bp.route('/select_playlist', methods=['POST'])
def select_playlist():
    # Ottieni i dati della playlist dal form
    playlist_id = request.form.get('playlist_id')
    playlist_name = request.form.get('playlist_name')

    if not playlist_id or not playlist_name:
        flash("Errore: Dati della playlist mancanti.")
        return redirect(url_for('home.home'))

    # Salva l'ID della playlist nella sessione (o in un'altra struttura dati)
    if 'selected_playlists' not in session:
        session['selected_playlists'] = []

    # Aggiungi la playlist selezionata alla sessione
    session['selected_playlists'].append({'id': playlist_id, 'name': playlist_name})
    flash(f"Playlist '{playlist_name}' selezionata con successo!")

    # Controlla se ci sono due playlist selezionate
    if len(session['selected_playlists']) == 2:
        return redirect(url_for('home.compare_playlists'))

    return redirect(url_for('home.home'))

@home_bp.route('/compare_playlists', methods=['GET'])
def compare_playlists():
    # Recupera le playlist selezionate dalla sessione
    selected_playlists = session.get('selected_playlists', [])

    if len(selected_playlists) < 2:
        flash("Seleziona almeno due playlist per confrontarle.")
        return redirect(url_for('home.home'))

    # Ottieni i dati delle due playlist
    playlist1 = selected_playlists[0]
    playlist2 = selected_playlists[1]

    # Recupera i dati delle playlist da Spotify
    sp = get_spotify_client()
    try:
        playlist1_data = sp.playlist(playlist1['id'])
        playlist2_data = sp.playlist(playlist2['id'])

        # Estrai i brani dalle playlist
        playlist1_tracks = {track['track']['name'] for track in playlist1_data['tracks']['items'] if track.get('track')}
        playlist2_tracks = {track['track']['name'] for track in playlist2_data['tracks']['items'] if track.get('track')}

        # Calcola i dati reali
        playlist1_total = len(playlist1_tracks)
        playlist2_total = len(playlist2_tracks)
        common_tracks = len(playlist1_tracks.intersection(playlist2_tracks))
        similarity_percentage = (common_tracks / min(playlist1_total, playlist2_total)) * 100 if min(playlist1_total, playlist2_total) > 0 else 0

    except Exception as e:
        flash(f"Errore nel recupero delle playlist: {e}")
        return redirect(url_for('home.home'))

    # Resetta la lista delle playlist selezionate
    session['selected_playlists'] = []

    return render_template(
        'brani_in_comune.html',
        playlist1_name=playlist1['name'],
        playlist2_name=playlist2['name'],
        playlist1_total=playlist1_total,
        playlist2_total=playlist2_total,
        common_tracks=common_tracks,
        similarity_percentage=similarity_percentage
    )