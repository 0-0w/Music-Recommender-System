import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "d539054ff49947059f39098d8b7a78ca"
CLIENT_SECRET = "9148e5835383424a91b2ea7e31b4831e"

client_credientials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credientials_manager)

df = pickle.load(open("df","rb"))
similarity = pickle.load(open("similarity","rb"))


def get_song_album_cover_url(song_name, artist):
    search_query = f"track:{song_name} artist:{artist}"
    results = sp.search(q=search_query, type="track")

    if results and results['tracks']['items']:
        track = results['tracks']['items'][0]
        album_cover_url = track['album']['images'][0]['url']
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://unsplash.com/photos/green-and-white-logo-illustration-JlO3-oY5ZlQ"
    


def recommender(song_name):
    idx = df[df["song"] == song_name].index[0]
    distance = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
    song = []
    recommender_music_poster = []
    recommender_song_name = []
    for i in distance[1:6]:
        artist = df.iloc[i[0]].artist
        print(artist)
        print(df.iloc[i[0]].song)
        recommender_music_poster.append(get_song_album_cover_url(df.iloc[i[0]].song,artist))
        recommender_song_name.append(df.iloc[i[0]].song)
    return recommender_song_name,recommender_music_poster


st.header('Music Recommender System')
music_list = df["song"].values

selected_music = st.selectbox("Type or select a music from dropdown ",music_list)

if st.button("Show recommendations"):
    recommended_music_names , recommended_music_poster = recommender(selected_music)
    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.text(recommended_music_names[0])
        st.image(recommended_music_poster[0])
    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_poster[1])
    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_poster[2])
    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_poster[3])
    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_poster[4])


