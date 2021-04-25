import requests 

BASE = "http://127.0.0.1:5000/"

data = [
        {"likes": 78, "name": "Joe", "views": 100000},
        {"likes": 1000, "name": "How to make Rest API", "views": 800000},
        {"likes": 10, "name": "Trini", "views": 100000},
        {"likes": 35, "name": "Trini", "views": 200},
]

'''for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())'''

'''response = requests.post(BASE + "artists", {"name": "trini", "age": 24})
print(response.json())
input()
response = requests.get(BASE + "artists")
print(response.json())
input()
response = requests.get(BASE + "artists/a2lsbGk=")
print(response.json())
'''
response = requests.get(BASE + "artists")
print(response.json())
input()
'''response = requests.delete(BASE + "artists/a2lsbGk=")
print(response.json())
response = requests.get(BASE + "artists")
print(response.json())
input()'''

'''response = requests.patch(BASE + "video/2", {"views":99, "likes":101})
print(response.json())'''
