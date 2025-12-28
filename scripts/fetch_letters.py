import urllib.request, json

url = 'http://127.0.0.1:5001/api/letters'
print('Fetching', url)
resp = urllib.request.urlopen(url).read().decode()
print(json.dumps(json.loads(resp), indent=2))
