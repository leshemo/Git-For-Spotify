#curl Req for access token: curl -X POST "https://accounts.spotify.com/api/token" -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=client_credentials&client_id=CLIENT-ID&client_secret=CLIENT-SECRET"
#my user id: 1el8m6u0rmvz8u6qc5eajnxu0


import json
from types import SimpleNamespace
data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'

x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
print(x.name, x.hometown.name, x.hometown.id)


#first, get new access token from spotify using client id and client secret

#make an api call to the spotify api to get a new access token using the client id and client secret



#then use that to query api for list of playlist ids

#iterate through list of ids and query the specific api endpoint for that playlist "https://api.spotify.com/v1/playlists/PLAYLIST_ID/tracks"
# grab added_at, track.album.name, track.artist.name, track.name, track.uri (through request fields)
#items(added_at,track(name,uri,album(name),artists(name)))

#add that to some data structure

