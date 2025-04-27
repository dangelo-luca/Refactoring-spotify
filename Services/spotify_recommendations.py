from Services.spotify_oauth import get_spotify_client

# Funzione che usa l'API di Spotify per ottenere raccomandazioni
def get_recommendations(seed_artists=None, seed_tracks=None, seed_genres=None):
    sp = get_spotify_client()
    
    # Debug: Stampa i parametri ricevuti
    print(f"Parametri originali: artists={seed_artists}, tracks={seed_tracks}, genres={seed_genres}")
    
    # Verifica che almeno uno dei parametri sia fornito
    if not any([seed_artists, seed_tracks, seed_genres]):
        print("Nessun parametro di seed fornito")
        return []
    
    # Prepara i parametri
    params = {'limit': 10}
    
    # Aggiungi i parametri solo se sono stati forniti
    if seed_artists:
        # Converti eventuali stringhe separate da virgole in lista
        if isinstance(seed_artists, str):
            artists = [a.strip() for a in seed_artists.split(',') if a.strip()]
            # Verifica la validità degli ID degli artisti
            valid_artists = []
            for artist_id in artists:
                try:
                    # Verifica se l'artista esiste
                    artist = sp.artist(artist_id)
                    valid_artists.append(artist_id)
                    print(f"Artista valido: {artist['name']} ({artist_id})")
                except Exception as e:
                    print(f"ID artista non valido: {artist_id}, errore: {e}")
            
            if valid_artists:
                params['seed_artists'] = valid_artists
    
    if seed_tracks:
        if isinstance(seed_tracks, str):
            tracks = [t.strip() for t in seed_tracks.split(',') if t.strip()]
            # Verifica la validità degli ID delle tracce
            valid_tracks = []
            for track_id in tracks:
                try:
                    track = sp.track(track_id)
                    valid_tracks.append(track_id)
                    print(f"Traccia valida: {track['name']} ({track_id})")
                except Exception as e:
                    print(f"ID traccia non valido: {track_id}, errore: {e}")
            
            if valid_tracks:
                params['seed_tracks'] = valid_tracks
    
    if seed_genres:
        if isinstance(seed_genres, str):
            # Ottieni i generi disponibili
            try:
                available_genres = sp.recommendation_genre_seeds()['genres']
                print(f"Generi disponibili: {available_genres}")
                
                # Filtra solo i generi validi
                genres = [g.strip().lower() for g in seed_genres.split(',') if g.strip()]
                valid_genres = [g for g in genres if g in available_genres]
                
                if valid_genres:
                    print(f"Generi validi: {valid_genres}")
                    params['seed_genres'] = valid_genres
                else:
                    print(f"Nessun genere valido tra quelli forniti: {genres}")
            except Exception as e:
                print(f"Errore nel recupero dei generi: {e}")
    
    # Verifica che ci sia almeno un seed valido
    if not any(key.startswith('seed_') for key in params):
        print("Nessun seed valido dopo la verifica")
        return []
    
    # Debug: Stampa i parametri finali
    print(f"Parametri finali per l'API: {params}")
    
    try:
        # Effettua la richiesta di raccomandazioni
        response = sp.recommendations(**params)
        return response['tracks'] if 'tracks' in response else []
    except Exception as e:
        print(f"Errore nelle raccomandazioni: {e}")
        return []
