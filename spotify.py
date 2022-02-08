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
