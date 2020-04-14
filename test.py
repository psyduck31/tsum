#coding=utf8
import requests, json



def addToCart(address, session):
	params = {"query": address}
	r = session.get("https://api.tsum.ru/location/location/suggest", params=params)
	print(r.status_code)
	print(r.text)


s = requests.Session()
s.headers = {}
addToCart("Россия, г Москва, ул Краснодарская, д 50", s)	