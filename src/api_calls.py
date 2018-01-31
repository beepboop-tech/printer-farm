import requests
import json

key = 'B5A36115A3DC49148EFC52012E7EBCD9'

headers = {
    'X-Api-Key': key
}


print(requests.get('http://10.11.12.166/api/files/local', headers=headers).json())
