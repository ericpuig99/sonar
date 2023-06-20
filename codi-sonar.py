import pandas as pd
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# Definim les claus d'autenticació per a l'API de Spotify
SPOTIPY_CLIENT_ID = ''  #autentifiquem
SPOTIPY_CLIENT_SECRET = ''

# Credencials de l'autenticador de SpotifyClientCredentials
auth_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)  # Crea una instància de l'objecte Spotify per interactuar amb l'API

playlist = '6ilUDRLkwZq4QTPZlzmHfx'  # ID de la playlist del sonar a analitzar

# Realitza la primera consulta per obtenir els primers 100 elements de la playlist
query = sp.playlist_items(playlist, fields=None, limit=100, offset=0, market=None)
# Realitza la segona consulta per obtenir els següents 100 elements de la playlist
query2 = sp.playlist_items(playlist, fields=None, limit=100, offset=100, market=None)

list_artistes = []  # Llista per guardar els artistes de les cançons
list_genres = []  # Llista per emmagatzemar els gèneres musicals
list_top_tracks = []  # Llista per emmagatzemar les cançons més populars dels artistes

# Bucle per obtenir els artistes principals de cada cançó de la primera consulta
for i in query["items"]:
    for artist in i["track"]["artists"]:
        artista = artist['name']
        list_artistes.append({"name": artist["name"], "id": artist['id']})
    time.sleep(0.1)  # Pausa de 0.1 segons per evitar superar els límits de l'API de Spotify

# Bucle per obtenir els artistes principals de cada cançó de la segona consulta
for j in query2["items"]:
    for artist in j["track"]["artists"]:
        artista = artist['name']
        list_artistes.append({"name": artist["name"], "id": artist['id']})
    time.sleep(0.1)  # Pausa de 0.1 segons per evitar superar els límits de l'API de Spotify

llista_df = []  # Llista per emmagatzemar els objectes DataFrame

# Bucle per obtenir les característiques de les cançons dels artistes
for a in list_artistes:
    query_artist = sp.artist(a['id'])  # Consulta per obtenir informació sobre l'artista

    query_toptracks = sp.artist_top_tracks(a['id'], country='ES')  # Consulta per obtenir les cançons més populars de l'artista

    artist_name = a['name']  # Nom de l'artista
    artist_genre = query_artist["genres"]  # Gèneres musicals de l'artista

    top_tracks_features = []  # Llista per guardar les característiques de les cançons
    top_tracks_name = []  # Llista per emmagatzemar els noms de les cançons

    for track in query_toptracks['tracks']:
        track_features = pd.DataFrame.from_dict(sp.audio_features(track['id']), orient="columns")  # Característiques de la cançó
        df = pd.DataFrame({"Artista": artist_name, "Nom Track": track['name']}, index=[0])  # DataFrame amb les dades de la cançó
        llista_df.append(pd.concat([df, track_features], axis=1))  # Afegir el DataFrame a la llista

df_final = pd.concat(llista_df)  # DataFrame final amb totes les dades
df_final.to_csv("Analisi Sonar.csv", index=False)  # Exporta les dades a un fitxer CSV
