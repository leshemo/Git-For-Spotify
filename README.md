# Git for Spotify

Spotify does not have any kind of history for the contents of a library, such as playlists or saved albums.

This project combines a script that checks for changes in a user's Spotify library (this script looks for only a couple playlists in my library and the saved albums, but that is not necessary for others) with a GitHub Action that runs the script every day and pushes changes to the repo itself, using the structure of Git to track changes in the playlist or the saved albums and saving them in a Markdown file, stored in the History directory.

This repo is forked from Ethan Rosenthal's project for some help with accessing the Spotify API (user authentication and whatnot). 

Future Plans:
- Implement Action that can create a new playlist from a past version of a playlist
- Create website that displays the changes over time
