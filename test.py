import requests 

BASE = "http://127.0.0.1:5000/"

# Crear artistas
response = requests.post(BASE + "artists", {"name": "new artist", "age": 30})
print(response.json())
input()

response = requests.get(BASE + "artists")
print(response.json())
input()

# Crear Albums
'''response = requests.post(BASE + "artists/ZGFtaWFu/albums", {"name": "album dami", "genre": "rock"})
print(response.json())
input()

response = requests.get(BASE + "artists/ZGFtaWFu/albums")
print(response.json())
input()

# Crear Tracks
response = requests.post(BASE + "albums/YWxidW0gZGFtaTpaR0Z0YV/tracks", {"name": "primer track", "duration": 3})
print(response.json())
input()

response = requests.post(BASE + "albums/YWxidW0gZGFtaTpaR0Z0YV/tracks", {"name": "segundo track", "duration": 3})
print(response.json())
input()

response = requests.get(BASE + "albums/YWxidW0gZGFtaTpaR0Z0YV/tracks")
print(response.json())
input()'''

# Get tracks from artist

'''response = requests.get(BASE + "artists/ZGFtaWFu/tracks")
print(response.json())'''

# delete album
#response = requests.delete(BASE + "albums/YWxidW0gZGFtaTpaR0Z0YV")

# Delete Artist
# response = requests.delete(BASE + "artists/ZGFtaWFu")

