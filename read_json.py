#%%
import json
import pandas as pd


def flatten_json(json_obj, parent_key='', separator='.'):
    """
    Aplana un objeto JSON anidado convirtiéndolo en un diccionario unidimensional.

    Parámetros:
    - json_obj (dict): El objeto JSON que se desea aplanar.
    - parent_key (str): El prefijo utilizado para mantener un registro del "padre" de las claves.
    - separator (str): El carácter utilizado para separar las claves en el nuevo diccionario.

    Retorna:
    - dict: Un diccionario unidimensional representando el objeto JSON aplanado.
    """
    flattened = {}
    for key, value in json_obj.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            flattened.update(flatten_json(value, new_key, separator=separator))
        else:
            flattened[new_key] = value
    return flattened

# Ruta al archivo JSON
archivo_json = 'taylor_swift_spotify.json'

# Abrir y leer el archivo JSON
with open(archivo_json, 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)

# Crear listas para almacenar los datos
data_list = []

# Iterar sobre los álbumes y las pistas
for album in datos["albums"]:
    album_id = album["album_id"]
    album_name = album["album_name"]
    album_release_date = album["album_release_date"]
    album_total_tracks = album["album_total_tracks"]

    for track in album["tracks"]:
        # Aplanar la estructura anidada del objeto JSON
        flattened_track = flatten_json(track)
        flattened_album = flatten_json(album)
        flattened_datos = flatten_json(datos)

        # Agregar la información a la lista
        flattened_track.update(flattened_album)
        flattened_track.update(flattened_datos)
        data_list.append(flattened_track)

# Crear el DataFrame final
df = pd.DataFrame(data_list)

column_order = ['disc_number', 'duration_ms', 'explicit', 'track_number',
                'track_popularity', 'track_id', 'track_name',
                'audio_features.danceability', 'audio_features.energy',
                'audio_features.key', 'audio_features.loudness', 'audio_features.mode',
                'audio_features.speechiness', 'audio_features.acousticness',
                'audio_features.instrumentalness', 'audio_features.liveness',
                'audio_features.valence', 'audio_features.tempo', 'audio_features.id',
                'audio_features.time_signature', 'artist_id', 'artist_name',
                'artist_popularity', 'album_id', 'album_name', 'album_release_date',
                'album_total_tracks']

df = df[column_order]
df.to_csv('dataset.csv', index= False)
#%%
