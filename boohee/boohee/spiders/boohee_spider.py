 #-*- coding: utf-8 -*-
import scrapy
from boohee.items import BooheeItem
class BooheeSpider(scrapy.Spider): 
	name = "boohee"
	def start_requests(self): 
		urls= ['http://www.boohee.com/food/group/'+str(i) for i in range(1,11)]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)
	def parse(self, response):
		foods = response.css('div.text-box')
		for food in foods:
			name=food.css('a::text')[0].extract()
			value=food.css('p::text').re(r'(\d+)')[0]
			yield BooheeItem({'name':name,'value':value})
		next_page=response.css('a.next_page::attr(href)').extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)