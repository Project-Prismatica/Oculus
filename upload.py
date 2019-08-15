import requests
import os

files = {'filename':open('tmp.jpg','rb')}
values = {'filename': 'tmp.jpg'}
url = "http://127.0.0.1:29001/api/up"


r = requests.post(url, files=files)
