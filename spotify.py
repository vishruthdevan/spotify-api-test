import pprint
import requests

pp = pprint.PrettyPrinter(indent=2)
queries = input("Enter n artist seperated by commas: ")
queries = [i.strip() for i in queries.split(',')]

CLIENT_ID = ""
CLIENT_SECRET = ""

BASE_URL = 'https://api.spotify.com/v1'
AUTH_URL = 'https://accounts.spotify.com/api/token'


auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
}).json()

access_token = auth_response['access_token']

HEADERS = {'Authorization': f'Bearer {access_token}'}


artist_ids = []
for i in queries:
    artists = requests.get(f"{BASE_URL}/search",
                           {"q": f"{i}", "type": "artist"}, headers=HEADERS)
    res = artists.json()
    # pp.pprint(res)
    artist_ids.append((res['artists']['items'][0]['name'],
                      res['artists']['items'][0]['id']))


data = {}


for artist_name, j in artist_ids:
    albums = requests.get(f"{BASE_URL}/artists/{j}/albums", headers=HEADERS)
    res = albums.json()

    for album in (res['items']):
        artist_data = {}
        album_data = {}
        album_name = album['name']
        album_date = album['release_date'][:4]
        album_id = album['id']

        song_data = []
        songs = requests.get(
            f"{BASE_URL}/albums/{album_id}/tracks", headers=HEADERS)
        for l in songs.json()['items']:
            song_data.append(l['name'])

        album_data[album_name] = song_data

# ----------------------------------------------------------------
        # if data.get(album_date, 0) == 0:
        #     data[album_date] = {artist_name: album_data}
        # else:
        #     data[album_date][artist_name] = album_data
# ----------------------------------------------------------------
        if data.get(album_date, 0) == 0:
            data[album_date] = {artist_name: [album_data]}
        else:
            if data[album_date].get(artist_name, 0) == 0:
                data[album_date][artist_name] = [album_data]
            else:
                data[album_date][artist_name].append(album_data)
# ------------------------------------------------------------------


# for year in sorted(data):
#     print(year)
#     for artist in data[year]:
#         print("  |---- ", artist)
#         for album in data[year][artist]:
#             print("             |---- ", album)
#             for song in data[year][artist][album]:
#                 print("                      |---- ", song)


for year in sorted(data):
    print(year)
    for artist in data[year]:
        print("  |---- ", artist)
        for album in data[year][artist]:
            print("             |---- ", list(album.keys())[0])
            for songs in album.values():
                for song in songs:
                    print("                      |---- ", song)
