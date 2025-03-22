import pandas as pd
import plotly.express as px
from plotly.io import to_html

# Supponiamo di avere un DataFrame con i dati
data = {
    'artist': ['Artist1', 'Artist2', 'Artist3', 'Artist4', 'Artist5', 'Artist6'],
    'album': ['Album1', 'Album2', 'Album3', 'Album4', 'Album5', 'Album6'],
    'genre': ['Pop', 'Rock', 'Jazz', 'Pop', 'Rock', 'Jazz'],
    'plays': [100, 200, 150, 300, 250, 50]
}
df = pd.DataFrame(data)

# Top 5 artisti
top_artists = df.groupby('artist')['plays'].sum().nlargest(5).reset_index()
fig1 = px.bar(top_artists, x='artist', y='plays', title='Top 5 Artisti', color='artist')

# Top 5 album
top_albums = df.groupby('album')['plays'].sum().nlargest(5).reset_index()
fig2 = px.bar(top_albums, x='album', y='plays', title='Top 5 Album', color='album')

# Distribuzione dei generi musicali
genre_distribution = df['genre'].value_counts().reset_index()
genre_distribution.columns = ['genre', 'count']
fig3 = px.pie(genre_distribution, names='genre', values='count', title='Distribuzione dei Generi Musicali')

# Esporta i grafici come stringhe HTML
fig1_html = to_html(fig1, full_html=False)
fig2_html = to_html(fig2, full_html=False)
fig3_html = to_html(fig3, full_html=False)