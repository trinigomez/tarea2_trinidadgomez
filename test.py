import requests 

BASE = "http://127.0.0.1:5000/"

'''response = requests.post(BASE + "artists", {"name": "damian", "age": 26})
print(response.json())
input()

response = requests.get(BASE + "artists")
print(response.json())
input()'''

response = requests.get(BASE + "albums/dHJpIGFsYnVtOmRISnA=/tracks")
print(response.json())
input()

response = requests.put(BASE + "albums/dHJpIGFsYnVtOmRISnA=/play")

response = requests.get(BASE + "albums/dHJpIGFsYnVtOmRISnA=/tracks")
print(response.json())
input()


'''response = requests.post(BASE + "artists/dHJp/albums", {"name": "segundo album", "genre": "rock"})
print(response.json())
input()

response = requests.get(BASE + "artists/dHJp/albums")
print(response.json())
input()'''

'''response = requests.post(BASE + "albums/dHJpIGFsYnVtOmRISnA=/tracks", {"name": "segundo track", "duration": 2})
print(response.json())
input()

response = requests.get(BASE + "albums/dHJpIGFsYnVtOmRISnA=/tracks")
print(response.json())
input()'''

'''
response = requests.post(BASE + "artists/ZGFtaWFu/albums", {"name": "primer album", "genre": "pop"})
print(response.json())'''


'''response = requests.patch(BASE + "video/2", {"views":99, "likes":101})
print(response.json())'''
