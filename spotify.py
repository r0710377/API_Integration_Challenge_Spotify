import urllib.parse
import requests
import json

# User credentials

c_id = 'your client ID'
c_secret = 'your client secret ID'

auth = 'https://accounts.spotify.com/api/token'

url = 'https://api.spotify.com/v1/artists/'

# Authorization credentials flow om te communiceren met de spotify API

auth_response = requests.post(auth, {
    'grant_type': 'client_credentials',
    'client_id': c_id,
    'client_secret': c_secret,
})

# Response wordt omgezet naar JSON

auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

# Access token

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# Access token (nodig voor tests)
# print(access_token) --> uncomment deze lijn om je token te zien

# De gebruiker de keuze geven om te zoeken of te annuleren

print("------------------")
print('Druk a om te zoeken')
print('Druk q om te annuleren')
print("------------------")

keuze = input("Keuze: ")

# Zolang je niet q typt, herhaalt de loop zich

while not (keuze == "q"):

    if keuze == "q":
        break
    
    if keuze == "a":

        # Gebruiker geeft naam artiest

        artiest = input("Over welke artiest wil je meer weten? ")

        if artiest == "q":
            break

        # De gegeven artiest wordt opgevraagd via search

        search = requests.get('https://api.spotify.com/v1/search', 
                 headers=headers, 
                 params={'q': artiest, 'type': 'artist'})
        
        # De output wordt omgezet naar json formaat

        search_dump = search.json()

        # Het ID, de followers en genres van de artiest worden ge-extract en opgeslagen in een variable

        artiest_id = search_dump['artists']['items'][0]['id']

        followers = search_dump['artists']['items'][0]['followers']['total']

        genres = search_dump['artists']['items'][0]['genres']

        # De data wordt geprint

        print("------------------")
        print("Voor algemene info, druk 1")
        print("Voor albums, druk 2")
        print("Voor top-tracks, druk 3")
        print("------------------")
        print("Om te annuleren, druk q")
        print("------------------")

        # Er wordt verder gevraagd wat je precies wil weten

        info = input("Wat wil je weten? ")

        # Zolang je niet q typt, herhaalt de loop zich

        while not (info == "q"):

            if info == "q":
                break

            # Indien je voor 1 koos, krijgje de algemene informatie te zien
    
            if info == "1":
            
                print("------------------")
                print("Algemene informatie over", artiest)
                print("------------------")
                print(artiest, "heeft", followers, "volgers")
                print("------------------")
                print("Meest voornamelijke genres:")
                print("------------------")
        
                for genre in genres:
                    print(genre)

                print("------------------")
                break

            if info == "2":
            
                # De albums van de artiest worden opgevraagd door middel van de net verkregen ID

                search_albums = requests.get(url + artiest_id + '/albums', 
                        headers=headers, 
                        params={'include_groups': 'album', 'limit': 10})

                # De output wordt omgezet naar json formaat

                albums_dump = search_albums.json()

                # Elk album wordt afgeprint

                print("------------------")
                print("Alle albums van", artiest)
                print("------------------")

                for album in albums_dump['items']:
                    print(album['name'], ' --- ', album['release_date'])

                print("------------------")
                break

        
            if info == "3":

                # De top-tracks van de artiest in Belgie worden opgevraagd

                tracks_search = requests.get(url + artiest_id + '/top-tracks', 
                        headers=headers,
                        params={'market': 'BE'})

                # De output wordt omgezet naar json formaat

                tracks_dump = tracks_search.json()

                # De naam en duratie van elke track wordt afgeprint

                print("------------------")
                print("De beste tracks van", artiest, "In Belgie")
                print("------------------")

                for track in tracks_dump['tracks']:
                    print(track['name'], " --- ", track['duration_ms'])

                print("------------------")
                break