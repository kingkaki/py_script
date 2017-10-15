#coding:utf8
import requests
from collections import Iterator,Iterable

class WeatherIterator(Iterator):
	def __init__(self,cities):
		self.cities=cities
		self.index=0

	def getweather(self,city):
		r=requests.get(u'http://wthrcdn.etouch.cn/weather_mini?city='+city)
		data=r.json()['data']['forecast'][0]
		return '%s:%s,%s'%(city,data['low'],data['high'])

	def next(self):
		if self.index==len(self.cities):
			raise StopIteration
		city=self.cities[self.index]
		self.index+=1
		return self.getweather(city)

class WeatherIterable(Iterable):
	def __init__(self,cities):
		self.cities=cities

	def __iter__(self):
		return WeatherIterator(self.cities)


for x in WeatherIterable([u'上海',u'株洲',u'台州',u'杭州',u'长沙']):
	print x





