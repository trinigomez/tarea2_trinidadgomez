import requests 

BASE = "http://127.0.0.1:5000/"

'''
response = requests.post(BASE + "artists", {"name": "Polima WestCoast", "age":21})
print(response.json())'''

response = requests.get(BASE + "artists/UG9saW1hIFdlc3RDb2FzdA==")
print(response.json())
input()

'''
response = requests.post(BASE + "artists/ZGFtaWFu/albums", {"name": "primer album", "genre": "pop"})
print(response.json())'''


'''response = requests.patch(BASE + "video/2", {"views":99, "likes":101})
print(response.json())'''
