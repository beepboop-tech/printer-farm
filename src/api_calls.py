import requests
import json

key = 'B5A36115A3DC49148EFC52012E7EBCD9'
# key = 'ED7F718BBE11456BA3619A04C66EF74A'

headers = {
    'X-Api-Key': key
}


print(requests.get('http://192.168.0.201/api/printer', headers=headers).json())
