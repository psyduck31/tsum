#coding=utf8
import requests, json, time, random
from datetime import datetime
from bs4 import BeautifulSoup as soup


headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36", "X-Requested-With": "XMLHttpRequest", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate, br"}


class Bot:
	def __init__(self, url):
		self.url = url
		self.session = requests.Session()
		self.session.headers = headers
		start = time.time()
		self.accessPage()
		print(time.time() - start)


	def accessPage(self):
		try:
			response = self.session.get(self.url, timeout = 4)
			if response.status_code == 200:
				print(f"[{datetime.today().strftime('%H:%M:%S')}] удалось получить страницу, ищу размеры..!")
				sizes = []
				data = soup(response.text, 'html.parser')
				text = data.findAll('script', {"id": "frontend-state"})[-1].text
				text = json.loads(text.replace("&q;", "\""))
				data = text["SSR_STATE_KEY"][f"http://api.int.tsum.com/catalog/item{self.url.split('product')[1]}"]['body']['skuList']
				for size in data:
					if size['availabilityInStock'] == True:
						sizes.append(size['id'])
				if len(sizes) > 0:
					self.addToCart(10863982)
			else:
				print(response.status_code)
				return None
		except TimeoutError:
			print(f"[{datetime.today().strftime('%H:%M:%S')}] сайт упал... пытаюсь заново получить размеры!")
			return self.accessPage()


	def addToCart(self, sku):
		print(f"[{datetime.today().strftime('%H:%M:%S')}] пытаюсь добавить в корзину какой-то размер...!")
		try:
			r = self.session.post("https://api.tsum.ru/cart/item", data=json.dumps({"type": "sku", "id": sku}))
			if r.status_code == 200:
				print(f"[{datetime.today().strftime('%H:%M:%S')}] атк получилось, иду на чекаут...!")
				data = json.loads(r.text)
			elif r.status_code == 400:
				data = json.loads(r.text)
				if data.get('title'):
					if data['message'] == "Невозможно добавить позицию":
						print(f"[{datetime.today().strftime('%H:%M:%S')}] OOS..!")
			else:
				print(r.status_code, r.text)
		except ReadTimeout:
			print(f"[{datetime.today().strftime('%H:%M:%S')}] сайт упал... повторяю атк...!")
			return self.addToCart(self, sku)


	def getShippinngRate(self, address):
		pass
		params = {"query": address}
		r = self.session.get("https://api.tsum.ru/location/location/suggest", params=params, timeout=4)


	def submitAddress(self, id):
		pass


	def checkout(self):
		pass


Bot("https://www.tsum.ru/product/5478783-tekstilnye-krossovki-brunello-cucinelli-sinii")