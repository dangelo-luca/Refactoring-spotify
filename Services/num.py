import pandas as pd
import plotly.express as px
from Services.spotify_oauth import get_playlist_tracks  

def analyze_and_visualize(playlist_id):
    
    tracks = get_playlist_tracks(playlist_id)

    print("Esempio di dati restituiti da get_playlist_tracks:")
    print(tracks[:5])  # Mostra i primi 5 elementi

    print("Esempio di valori di durata:")
    print([track.get("duration") for track in tracks])

    # Filtra i brani con durate valide
    tracks = [track for track in tracks if track.get("duration") and track["duration"] != "0:00"]

    print("Brani con durate valide:")
    print(tracks[:5])

    if not tracks:
        print("Nessun dato disponibile per l'analisi.")
        return None

    data = [
        {
            "artist": track["artist"],
            "album": track["album"],
            "track_name": track["name"],
            "popularity": track.get("popularity", 0),
            "genre": track.get("genre", "Sconosciuto"),
            "duration": track.get("duration", "0:00"),
            "release_year": track.get("release_year", "Sconosciuto"),
            
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

    # Conteggio dei brani per anno di rilascio
    release_year_counts = df["release_year"].value_counts().reset_index()
    release_year_counts.columns = ["release_year", "count"]
    release_year_counts = release_year_counts.sort_values("release_year")

    # Creazione del grafico a barre
    fig_release_year = px.bar(
        release_year_counts,
        x="release_year",
        y="count",
        title="Distribuzione Temporale dei Brani",
        labels={"release_year": "Anno di Pubblicazione", "count": "Numero di Brani"},
        text="count"  # Mostra i valori sopra le barre
    )

    # Conversione della durata in minuti da millisecondi
    def convert_duration_to_minutes(duration_ms):
        try:
            return duration_ms / 60000  # Converti millisecondi in minuti
        except (TypeError, ValueError):
            print(f"Formato durata non valido: {duration_ms}")  # Debug per valori malformati
            return 0  # Valore predefinito per durate non valide

    # Applicazione della funzione e debug
    print("Durate originali (primi 5 valori):")
    print(df["duration"].head())  # Debug per verificare i dati originali

    df["duration_minutes"] = df["duration"].apply(convert_duration_to_minutes)

    print("Durate convertite in minuti (primi 5 valori):")
    print(df["duration_minutes"].head())  # Debug per verificare i risultati

    # Definizione dei bin e delle etichette per la durata
    bins = [0, 2, 4, 6, 8, 10, 15, 20]
    labels = ["<2", "<4", "<6", "<8", "<10", "<15", "<20"]
    df["duration_range"] = pd.cut(df["duration_minutes"], bins=bins, labels=labels, include_lowest=True)

    # Conteggio delle durate per intervallo
    duration_counts = df["duration_range"].value_counts().sort_index().reset_index()
    duration_counts.columns = ["duration_range", "count"]

    print("Conteggio per intervallo di durata:")
    print(duration_counts)

    # Creazione del grafico
    fig_duration = px.bar(
        duration_counts,
        x="duration_range",
        y="count",
        title="Distribuzione della Durata dei Brani",
        labels={"duration_range": "Intervallo di Durata (min)", "count": "Numero di Brani"},
        category_orders={"duration_range": labels}
    )

    df_filtered_years = df[df["release_year"].apply(lambda x: str(x).isdigit())].copy()
    df_filtered_years["release_year"] = df_filtered_years["release_year"].astype(int)

    popularity_by_year = df_filtered_years.groupby("release_year")["popularity"].mean().reset_index()

    fig_popularity_over_time = px.line(
        popularity_by_year,
        x="release_year",
        y="popularity",
        title="Evoluzione della Popolarità nel Tempo",
        labels={"release_year": "Anno di Pubblicazione", "popularity": "Popolarità Media"},
        markers=True
    )


    

    return {
        "fig_artists": fig_artists.to_html(full_html=False),
        "fig_albums": fig_albums.to_html(full_html=False),
        "fig_popularity": fig_popularity.to_html(full_html=False),
        "fig_genres_bar": fig_genres_bar.to_html(full_html=False),
        "fig_genres_pie": fig_genres_pie.to_html(full_html=False),
        "fig_release_year": fig_release_year.to_html(full_html=False),
        "fig_duration": fig_duration.to_html(full_html=False),
        "fig_popularity_over_time": fig_popularity_over_time.to_html(full_html=False),
    }
