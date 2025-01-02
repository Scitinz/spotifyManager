# spotifyManager
 
### Setup
Create an app in the spotify developer portal with the intended use as Web API. Copy the client ID and client secret into params.json. Set the redirect URI to match the one you set on the portal.

Create a virtual python environment with `python -m venv venv`

Install from requirements.txt with `pip install -r requirements.txt`

Run the app with `python main.py`

### Current Functionality

- Retrieve your spotify playlists and save them to a cache.
- Alter that cache (remove playlists).
- Load previously saved caches.
- See what songs exist in a playlist, but not in another.