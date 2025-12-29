import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import requests
import os

#set environment variables
os.system("export CLIENT_ID=CLIENT_ID_PLACEHOLDER")
os.system("export CLIENT_SECRET=CLIENT_SECRET_PLACEHOLDER")
os.system("export REDIRECT_URI=http://localhost:8080")

scope = "streaming,user-read-playback-state,user-library-read,user-modify-playback-state,app-remote-control"

client_id = "CLIENT_ID_PLACEHOLDER"
client_secret = "CLIENT_SECRET_PLACEHOLDER"
redirect_url = "http://localhost:8080"

def spotify_init():
    scope = "streaming,user-read-playback-state,user-library-read,user-modify-playback-state,app-remote-control"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_url, open_browser=False))
    device_id = sp.devices()["devices"][0]["id"]
    sp.transfer_playback(device_id)
    sp.pause_playback()
    return sp


def add_playlist_to_queue(sp):
    playlist = sp.current_user_playlists(limit = 50, offset = 0)["items"][0]
    play_list_id = playlist["id"]
    items = sp.playlist_items(play_list_id)
    tracks = items["items"]
    num_songs = len(tracks)
    first_id = tracks[0]["track"]["id"]
    for track in tracks:
        track_id = track["track"]["id"]
        sp.add_to_queue(track_id)
    # while(sp.queue()["currently_playing"]["id"] != first_id):
    #     sp.next_track()
    
    try:
        sp.start_playback()
    except:
        pass
    download_curr_album_cover(sp)
    # sp.seek_track(0)


def download_curr_album_cover(sp):
    album_cover_url = sp.current_playback()["item"]["album"]["images"][-1]["url"]
    response = requests.get(album_cover_url)
    with open("album_cover.jpg", 'wb') as f:
        f.write(response.content)



def get_curr_track_info(sp):
    curr_playback = sp.current_playback()
    artist = curr_playback["item"]["artists"][0]["name"]
    track_name = curr_playback["item"]["name"]
    return track_name, artist

# print(json.dumps(sp.current_playback(), indent = 4))
sp = spotify_init()
add_playlist_to_queue(sp)
print(get_curr_track_info(sp))