import spotipy
from spotipy.oauth2 import SpotifyOAuth

import json

with open("params.json") as f:
    vars = json.load(f)

scopes = ["user-library-read", "playlist-read-private", "playlist-modify-private", "playlist-modify-public"]

client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=vars["CLIENT_ID"], client_secret=vars["CLIENT_SECRET"], 
                                                   redirect_uri=vars["REDIRECT_URI"], scope=scopes))

working_cache = dict()

def save_working_cache(working_cache):
    with open("playlist_cache.json", "w") as f:
        json.dump(working_cache, f, indent=2)

def load_cached_playlists():
    with open("playlist_cache.json") as f:
        working_cache = json.load(f)
    return working_cache

def remove_playlist_from_cache_by_name(working_cache, name):
    for idx, item in enumerate(working_cache):
        if item['name'] == name:
            working_cache.pop(idx)
    return working_cache

def print_playlists(working_cache):
    for idx, item in enumerate(working_cache):
        print(str(idx) + " : " + item['name'])

def remove_playlist_from_cache_by_index(working_cache, index):
    working_cache.pop(index)
    return working_cache

def find_songs_in_a_not_in_b(a, b):
    missing_items = list()
    exists = False
    for i in range(0, len(a)):
        exists = False
        for j in range(0, len(b)):
            if a[i]['track']['id'] == b[j]['track']['id']:
                exists = True
        if exists == False:
            missing_items.append(a[i])
    
    for item in missing_items:
        print(item['track']['name'] + " : " + item['track']['id'])


working_cache

while True:
    print("\nOptions:")
    print("1 : Get Playlists")
    print("2 : Print Playlists")
    print("3 : Remove Playlist by name (from cache, not spotify)")
    print("4 : Remove Playlist by index")
    print("5 : Save Cached Playlists")
    print("6 : Load Cached Playlists")
    print("7 : Find items in Playlist A that are not in Playlist B")
    print("0 : Exit")

    choice = int(input("option: "))
    match choice:
        case 0:
            exit()
        case 1: 
            working_cache = client.current_user_playlists()['items']
        case 2:
            print_playlists(working_cache)
        case 3:
            name_to_remove = input("Name: ")
            remove_playlist_from_cache_by_name(working_cache, name_to_remove)
        case 4:
            index_to_remove = int(input("Index: "))
            remove_playlist_from_cache_by_index(working_cache, index_to_remove)
        case 5:
            save_working_cache(working_cache)
        case 6:
            working_cache = load_cached_playlists()
        case 7:
            playlist_a_index = int(input("Playlist A index: "))
            playlist_b_index = int(input("Playlist B index: "))
            append_items = list()
            playlist_a_songs = list()
            playlist_b_songs = list()
            loops = 0
            while True:
                append_items = client.playlist_items(playlist_id=working_cache[playlist_a_index]['id'], fields="total,items.track.name,items.track.id", limit=50, offset=loops*50)
                playlist_a_songs.extend(append_items['items'])
                if len(append_items['items']) < 50:
                    break
                loops += 1
            loops = 0
            while True:
                append_items = client.playlist_items(playlist_id=working_cache[playlist_b_index]['id'], fields="total,items.track.name,items.track.id", limit=50, offset=loops*50)
                playlist_b_songs.extend(append_items['items'])
                if len(append_items['items']) < 50:
                    break
                loops += 1

            find_songs_in_a_not_in_b(playlist_a_songs, playlist_b_songs)
        case _:
            continue

