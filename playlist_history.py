import datetime as dt
import logging
import os
import sys

from dotenv import dotenv_values
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


logger = logging.getLogger("discovered-weekly")
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter(fmt="%(asctime)s : %(levelname)s : %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def main():
    # Override sample with non-sample file-based env variables,
    # and override both with actual env variables
    config = {**dotenv_values("sample.env"), **dotenv_values(".env"), **os.environ}
    logger.info("Started daily playlist logging.")
    client = load_client(
        config["CLIENT_ID"],
        config["CLIENT_SECRET"],
        config["REDIRECT_URI"],
        config["USERNAME"],
        config["REFRESH_TOKEN"],
    )   

    for playlist_name in "Rap", "Jazz_Electronic", "Everything_Else":
        playlist_tracks = get_playlist_tracks(client,config[playlist_name])
        logger.info(f"Found {len(playlist_tracks)} tracks in playlist: {playlist_name}.")
        create_markdown_file(playlist_name, playlist_tracks)
    logger.info("Finished daily playlist logging.")


def load_client(client_id, client_secret, redirect_uri, username, refresh_token):
    scopes = ["playlist-read-private", "playlist-modify-private"]
    # Authenticate
    auth_manager = SpotifyOAuth(
        scope=scopes,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        username=username,
    )
    auth_manager.refresh_access_token(refresh_token)
    client = spotipy.Spotify(auth_manager=auth_manager)
    return client

#get tracks of one playlist, given a particular playlist id, accounting for the fact that my playlists are over 100 tracks long
def get_playlist_tracks(client,playlist_id):
    results = client.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = client.next(results)
        tracks.extend(results['items'])
    return tracks

#Creates or updates a markdown file for a given playlist
def create_markdown_file(playlist_name, playlist_tracks):
    playlist_string = "## Playlist Title \n|No. | Title | Artist(s) | Album | Date added | URI |\n |:--|:--|:--|:--|:--|:--|\n"
    for i, track in enumerate(playlist_tracks):
        track_name = track["track"]["name"].replace("|", "-")
        track_artists = ", ".join([artist["name"] for artist in track["track"]["artists"]]).replace("|", "-")
        album_name = track["track"]["album"]["name"].replace("|", "-")
        date_added = dt.datetime.strptime(track["added_at"], "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d")
        track_uri = track["track"]["uri"]
        playlist_string += f"| {i+1} | {track_name} | {track_artists} | {album_name} | {date_added} | <sub>{track_uri}</sub> |\n"

    filename = f"{playlist_name}.md"

    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(playlist_string)
            logger.info(f"No exisitng file found. A {playlist_name} playlist has been created.")
    else:
        with open(filename, "r+", encoding="utf-8") as f:
            existing = f.read()
            if existing != playlist_string:
                f.seek(0)
                f.write(playlist_string)
                f.truncate()
                logger.info(f"The {playlist_name} playlist has been updated.")
            else:
                logger.info(f"No changes were found.")
                logger.info(f"The {playlist_name} playlist has not been updated.")


# def parse_this_week(client, discover_weekly_playlist_id):

#     # Grab this week's Discover Weekly (DW) and parse for some info
#     dw_items = client.playlist_items(discover_weekly_playlist_id)
#     playlist_created = dt.datetime.strptime(
#         dw_items["items"][0]["added_at"], "%Y-%m-%dT%H:%M:%S%z"
#     )
#     playlist_date = playlist_created.strftime("%Y-%m-%d")

#     dw_uris = [item["track"]["uri"] for item in dw_items["items"]]
#     return playlist_date, dw_uris


# def add_to_all_time_playlist(client, dw_uris, all_discovered_playlist_id):
#     # First, add to the all time DW

#     # Determine total number of tracks
#     total = client.playlist(all_discovered_playlist_id)["tracks"]["total"]
#     # Now, query for the last 5 tracks
#     offset = max(0, total - 5)
#     last_five = client.playlist_items(all_discovered_playlist_id, offset=offset)
#     # If the last 5 tracks match the last 5 from the current week, then we've already added
#     # this week's playlist.
#     match = len(last_five["items"]) >= 5 and all(
#         [
#             dw_uri == item["track"]["uri"]
#             for dw_uri, item in zip(dw_uris[-5:], last_five["items"])
#         ]
#     )
#     if match:
#         logger.info(
#             "This script has already been run for this week."
#             " Skipping add to all time playlist."
#         )
#         return

#     client.playlist_add_items(all_discovered_playlist_id, dw_uris)


# def add_to_weekly_archive(client, username, playlist_date, dw_uris):
#     # Second, create the weekly archive playlist
#     this_weeks_playlist = f"Discovered Week {playlist_date}"

#     # Need to search all user's playlists to see if this one already exists...
#     limit = 50
#     offset = 0
#     total = 1e9
#     found = False

#     while offset + limit < total and not found:
#         playlists = client.user_playlists(username, limit=limit, offset=offset)
#         total = playlists["total"]
#         found = any(
#             [item["name"] == this_weeks_playlist for item in playlists["items"]]
#         )
#         offset += limit

#     if found:
#         logger.info(
#             "This script has already been run for this week."
#             " Skipping creation of weekly archive playlist."
#         )
#         return

#     logger.info(f"Creating this week's archive playlist: {this_weeks_playlist}")
#     saved_playlist = client.user_playlist_create(
#         username, this_weeks_playlist, public=False
#     )
#     client.playlist_add_items(saved_playlist["id"], dw_uris)
#     logger.info("Done creating this week's archive playlist.")


if __name__ == "__main__":
    main()
