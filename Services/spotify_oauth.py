import logging
from flask import session
import spotipy
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials
SPOTIFY_CLIENT_ID = "59eb1d0383344f50a12b1842a08ddfc2"
SPOTIFY_CLIENT_SECRET = "5d1d88ac19774b54810d3c52ad49c465"

SPOTIFY_REDIRECT_URI = "http://127.0.0.1:5000/callback"
client_id = "59eb1d0383344f50a12b1842a08ddfc2"
client_secret = "5d1d88ac19774b54810d3c52ad49c465"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))


sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-private", #permessi x informazioni dell'utente
    show_dialog=True
)

def get_spotify_object(token_info):
    return spotipy.Spotify(auth=token_info['access_token'])

def authenticate_user():
    auth_url = sp_oauth.get_authorize_url()
    print(f"Visita questo URL per autenticarti: {auth_url}")
    response = input("Inserisci l'URL di reindirizzamento dopo l'autenticazione: ")
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)
    return token_info

def get_spotify_client():
    token_info = session.get("token_info")

    if token_info:
        return spotipy.Spotify(auth=token_info.get("access_token"))  
    
   
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id="59eb1d0383344f50a12b1842a08ddfc2",
        client_secret="5d1d88ac19774b54810d3c52ad49c465"
        
    ))
    


def get_playlist_tracks(playlist_id):
    
    sp = get_spotify_client()
    try:
        results = sp.playlist_tracks(playlist_id)
        tracks = []

        for track in results["items"]:
            track_info = track["track"]
            if not track_info:  
                continue

           
            artists = track_info["artists"]
            artist_ids = [artist["id"] for artist in artists]

            
            genres = set()
            if artist_ids:
                artists_info = sp.artists(artist_ids)["artists"]
                for artist in artists_info:
                    genres.update(artist.get("genres", []))

            
            cover = None
            if track_info["album"]["images"]:
                cover = track_info["album"]["images"][0]["url"]  

            
            tracks.append({
                "name": track_info["name"],
                "artist": ", ".join(artist["name"] for artist in artists),
                "album": track_info["album"]["name"],
                "popularity": track_info.get("popularity", 0),
                "genre": ", ".join(genres) if genres else "Sconosciuto",  
                "cover": cover  
               
            })

        return tracks
    except Exception as e:
        logging.error(f"Errore durante il recupero dei brani della playlist: {e}")
        return []