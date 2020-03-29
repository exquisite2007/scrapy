import scrapy
import re
from coolshell.items import CoolshellItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
class coolshellSpider(scrapy.Spider):
    name = "coolshell"
    digit_pattern='\d+,?\d*'
    def start_requests(self):
        yield scrapy.Request(url='https://coolshell.cn/', callback=self.parse_article_list)
    def parse_article_list(self,response):
    	#extract article links
    	
    	for link_body in response.css('article'):
    		link=link_body.css('h2.entry-title a::attr(href)').get()
    		yield scrapy.Request(url=link, callback=self.parse_article)

    	# next page
    	next_page = response.css('a.nextpostslink::attr(href)').get()
    	if next_page is not None:
    		yield scrapy.Request(url=next_page, callback=self.parse_article_list)
    	response.css('a.nextpostslink')
    def parse_article(self,response):
    	loader = ItemLoader(item=CoolshellItem(), response=response)
    	loader.default_output_processor = TakeFirst()
    	loader.add_value('title',response.css('h1.entry-title::text').get())
    	loader.add_value('create_time',response.css('h5.entry-date time::attr(datetime)').get())
    	loader.add_value('author',response.css('h5.entry-date span.byline a::text').get())
    	comments_num=response.css('h5.entry-date a.comments-link::text').get()
    	comments_num_match=re.search(self.digit_pattern,comments_num)
    	loader.add_value('comments_num', '0' if comments_num_match is None else comments_num_match.group(0))

    	read_num=response.css('h5.entry-date::text').getall()[-1]
    	loader.add_value('read_num',re.search(self.digit_pattern,read_num).group(0))
    	loader.add_value('content','\n'.join(response.css('div.entry-content p::text').getall()[:-3]))
    	rate=response.css('div.post-ratings strong::text').getall()
    	loader.add_value('rate_num',rate[0] if len(rate)>0 else '0')
    	loader.add_value('rate_avg',rate[1] if len(rate)>0 else '0')
    	loader.add_value('url',response.url)
    	loader.add_value('tags',','.join(response.css('footer.entry-footer a::text').getall()))
    	yield loader.load_item()
