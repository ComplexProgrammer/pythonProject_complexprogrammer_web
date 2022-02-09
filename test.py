import requests, json

response = requests.get('http://172.20.0.31:4444/Api/C0mplexApi/GetExchangeRates').content
data = json.loads(response)
print(data)