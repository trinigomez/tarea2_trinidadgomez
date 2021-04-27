import requests 

BASE = "http://127.0.0.1:5000/"


response = requests.post(BASE + "artists", {"name": "Adele", "age":30})
print(response.json())
input()
response = requests.delete(BASE + "artists/QWRlbGU=")

input()

'''
response = requests.post(BASE + "artists/ZGFtaWFu/albums", {"name": "primer album", "genre": "pop"})
print(response.json())'''


'''response = requests.patch(BASE + "video/2", {"views":99, "likes":101})
print(response.json())'''
