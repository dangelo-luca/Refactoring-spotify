import spotipy
from spotipy.oauth2 import SpotifyOAuth
SPOTIFY_CLIENT_ID = "59eb1d0383344f50a12b1842a08ddfc2"
SPOTIFY_CLIENT_SECRET = "5d1d88ac19774b54810d3c52ad49c465"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:5000/callback"

#config SpotifyOAuth per l'autenticazione e redirect uri
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

