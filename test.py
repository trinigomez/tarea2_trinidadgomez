import requests 

BASE = "http://127.0.0.1:5000/"


response = requests.get(BASE + "tracks")
print(response.json())

'''response = requests.post(BASE + "artists", {"name":"damian", "age":26})
print(response.json())
input()
'''

response = requests.post(BASE + "artists/ZGFtaWFu/albums", {"name": "primer album", "genre": "pop"})
print(response.json())


'''response = requests.patch(BASE + "video/2", {"views":99, "likes":101})
print(response.json())'''
