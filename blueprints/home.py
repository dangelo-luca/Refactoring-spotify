from flask import Blueprint, render_template, redirect, url_for, session,request
from Services.spotify_oauth import get_spotify_object
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
home_bp = Blueprint('home', __name__)


'''@home_bp.route('/')
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

    return render_template('artisti.html', artists=artists)'''

def get_spotify_client():
    token_info = session.get("token_info")

    if token_info:
        return spotipy.Spotify(auth=token_info.get("access_token"))  
    
   
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id="59eb1d0383344f50a12b1842a08ddfc2",
        client_secret="5d1d88ac19774b54810d3c52ad49c465"
    ))

@home_bp.route("/", methods=["GET", "POST"])
def home():
    sp = get_spotify_client() 
    
    user_info, playlists = None, []
    
   
    if isinstance(sp, spotipy.Spotify) and session.get("token_info"):
        try:
            user_info = sp.current_user()
            playlists = sp.current_user_playlists()["items"]
        except Exception:
            pass  
    
    search_results = []
    query = ""
    
    
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            try:
                
                if not isinstance(sp, spotipy.Spotify):
                    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                        client_id="59eb1d0383344f50a12b1842a08ddfc2", 
                        client_secret="5d1d88ac19774b54810d3c52ad49c465"  
                    ))
                
                results = sp.search(q=query, type="playlist", limit=10)
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
    
    return render_template("home.html", user_info=user_info, playlists=playlists, query=query, search_results=search_results)

@home_bp.route("/playlist/<playlist_id>")
def playlist(playlist_id):
    sp = get_spotify_client() 
    
    if not isinstance(sp, spotipy.Spotify):
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id="59eb1d0383344f50a12b1842a08ddfc2",  
            client_secret="5d1d88ac19774b54810d3c52ad49c465"  
        ))

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

    return render_template("playlist.html", playlist=playlist_data, tracks=tracks)