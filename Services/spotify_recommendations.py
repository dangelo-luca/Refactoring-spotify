from Services.spotify_oauth import get_spotify_client

# Funzione che usa l'API di Spotify per ottenere raccomandazioni
def get_recommendations(seed_artists=None, seed_tracks=None, seed_genres=None, limit=10):
    sp = get_spotify_client()  # Otteniamo il client autenticato

    # Prepariamo i parametri
    recommendations = sp.recommendations(
        seed_artists=seed_artists.split(",") if seed_artists else None,
        seed_tracks=seed_tracks.split(",") if seed_tracks else None,
        seed_genres=seed_genres.split(",") if seed_genres else None,
        limit=limit
    )

    # Estraiamo le informazioni utili dalle tracce consigliate
    tracks = []
    for track in recommendations['tracks']:
        tracks.append({
            "id": track['id'],
            "name": track['name'],
            "artists": ", ".join(artist['name'] for artist in track['artists']),
            "album": track['album']['name'],
            "cover": track['album']['images'][0]['url'] if track['album']['images'] else None,
            "preview_url": track['preview_url']
        })

    return tracks
