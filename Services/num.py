import pandas as pd
import plotly.express as px
from Services.spotify_oauth import get_playlist_tracks  

def analyze_and_visualize(playlist_id):
    
    tracks = get_playlist_tracks(playlist_id)

    if not tracks:
        print("Nessun dato disponibile per l'analisi.")
        return None

    data = [
        {
            "artist": track["artist"],
            "album": track["album"],
            "track_name": track["name"],
            "popularity": track.get("popularity", 0),
            "genre": track.get("genre", "Sconosciuto") 
        }
        for track in tracks
    ]

    df = pd.DataFrame(data)

    if df.empty:
        print("DataFrame vuoto, impossibile generare il grafico.")
        return None

    # Top 5 artisti più popolari
    top_artists = df.groupby("artist")["popularity"].sum().nlargest(5).reset_index()
    fig_artists = px.bar(top_artists, x="artist", y="popularity", title="Top 5 Artisti più popolari")

    # Top 5 album più popolari
    top_albums = df.groupby("album")["popularity"].sum().nlargest(5).reset_index()
    fig_albums = px.bar(top_albums, x="album", y="popularity", title="Top 5 Album più popolari")

    # Distribuzione della popolarità (istogramma)
    fig_popularity = px.histogram(df, x="popularity", nbins=10, title="Distribuzione della Popolarità")

    # Distribuzione dei generi musicali (grafico a barre)
    genre_counts = df["genre"].str.split(", ", expand=True).stack().value_counts().reset_index()
    genre_counts.columns = ["genre", "count"]
    genre_counts = genre_counts[genre_counts["genre"] != "Sconosciuto"]
    fig_genres_bar = px.bar(genre_counts, x="genre", y="count", title="Distribuzione dei Generi Musicali")

    # Grafico a torta per la distribuzione dei generi musicali
    fig_genres_pie = px.pie(
        genre_counts,
        names="genre",
        values="count",
        title="Distribuzione dei Generi Musicali",
        labels={"genre": "Genere", "count": "Numero di brani"}
    )

    return {
        "fig_artists": fig_artists.to_html(full_html=False),
        "fig_albums": fig_albums.to_html(full_html=False),
        "fig_popularity": fig_popularity.to_html(full_html=False),
        "fig_genres_bar": fig_genres_bar.to_html(full_html=False),
        "fig_genres_pie": fig_genres_pie.to_html(full_html=False),
    }
