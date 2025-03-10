
from flask import Blueprint, jsonify, render_template,redirect,session,url_for,request
from Services.spotify_oauth import sp_oauth
from Services.spotify_oauth import get_spotify_object


artisti_bp = Blueprint("artisti", __name__)

@artisti_bp.route('/artisti')
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
    user_info = sp.current_user()

    return render_template('artisti.html',user_info=user_info,  artists=artists)    