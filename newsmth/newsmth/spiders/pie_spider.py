import scrapy
class PieSpider(scrapy.Spider):
    name = "newsmth"
    MAX_PAGE=10
    BOARD='Career_Upgrade'
    def start_requests(self):
        
        yield scrapy.Request(url='http://www.newsmth.net/', callback=self.login_parse)
    def login_parse(self,response):
    	for i in range(self.MAX_PAGE):
    		yield scrapy.Request(url='http://www.newsmth.net/nForum/board/{}?ajax&p={}'.format(self.BOARD,i+1), callback=self.pie_parse)
    def pie_parse(self,response):
    	remove_top_lst=filter(lambda x:len(x.css('tr.top'))==0,response.css('tbody tr'))
    	for x in list(remove_top_lst):
    		url=x.css('td')[0].css('td a::attr(href)').get()
    		title=x.css('td')[1].css('td a::text').get()
    		create_date=x.css('td')[2].css('*::text').get()
    		author=x.css('td')[3].css('td a::text').get()
    		score=x.css('td')[4].css('td *::text').get()
    		like=x.css('td')[5].css('td *::text').get()
    		reply_num=x.css('td')[6].css('td *::text').get()
    		last_reply_date=x.css('td')[7].css('td a::text').get()
    		print('{} {} {} {} {} {} {} {}'.format(url,title,create_date,author,score,like,reply_num,last_reply_date))
    	
    