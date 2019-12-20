import scrapy
from news.items import NewsItem
class C114RootSpider(scrapy.Spider): 
	name = "c114"
	base_url='http://www.c114.com.cn/search/?q=5G&p={}&addtime=15&r=0&source=0&search=0'
	def start_requests(self): 
	#参数addtime是截止日期，15表示15天内的
		url=self.base_url.format(1)
		yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		#titles=response.css("div.s2 h3 a::text").getall()
		digests=response.css("div.s2 p.t::text").getall()
		links=response.css("div.s2 h3 a::attr(href)").getall()		
		for i in list(zip(links,digests)):
			yield scrapy.Request(i[0], callback=self.parse2,meta={'digest':i[1]})
		next_page_num=response.css("div.page a")[-1].re(r'(\d+)')[0]
		if next_page_num is not None:
			yield scrapy.Request(self.base_url.format(next_page_num), callback=self.parse)
	def parse2(self,response):#去子链接查看日期
		title=response.css('h1::text').get()
		digest= response.meta['digest']
		#digest=''.join(response.css('div.text p')[0].css('*::text').getall())
		link=response.url
		ts=response.css('div.r_time::text').get()
		yield NewsItem(a_title=title,b_digest=digest,c_link=link,d_ts=ts)
