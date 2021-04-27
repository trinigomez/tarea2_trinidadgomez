import requests 

BASE = "http://127.0.0.1:5000/"

'''response = requests.post(BASE + "artists/VHJpbmlkYWQ=/albums", {"name": "tri album", "genre":"pop"})
print(response.json())
input()'''
response = requests.get(BASE + "albums/dHJpIGFsYnVtOlZISnBibWxrWVdRPQ==")
print(response.json())
input()

'''
response = requests.post(BASE + "artists/ZGFtaWFu/albums", {"name": "primer album", "genre": "pop"})
print(response.json())'''


'''response = requests.patch(BASE + "video/2", {"views":99, "likes":101})
print(response.json())'''
