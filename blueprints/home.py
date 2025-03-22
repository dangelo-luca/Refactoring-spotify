from flask import Blueprint, render_template, redirect, url_for, session,request
from Services.spotify_oauth import get_spotify_object , get_spotify_client
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from models import db, Playlist
from flask_login import login_required, current_user
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

    return render_template("playlist.html", user_info=user_info, playlist=playlist_data, tracks=tracks)

