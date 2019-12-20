# scrapy
scrapy入门
最近项目需要爬一些东西，试了一把大名鼎鼎的scrapy,确实好用，很简单

1.先看官方文档   

2.安装python环境virtualenv   

virtualenv是我在这里学到的不错的工具。可以创建独立的python环境。比如，有些项目会用到python3,有的会用到python2.7，如果底层依赖的包同名，或者有其它python项目依赖的与你当前项目不同，就会有冲突或者两个项目的依赖就有干绕。
通过virtualenv就可以创建互不干绕的环境。其原理是将所有依赖包放到一个指定目录下，然后启动的shell就依赖在这个环境里了。
```
pip install virtualenv
virtualenv  NEWDIR
cd NEWDIR
source bin/active
pip install scrapy
```
通过以上步骤就完成安装   

3.创建scrapy项目,这里我们以薄荷网为例，抓取食物的热量。因为PC网页只暴露一部分，所以该项目只能把暴露的部分抓下来。
```
scrapy startproject boohee

```
4.在spider目录下，创建spider
```
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
```
5.在items.py下加入Item class. Item class可用于存放从网页爬下来的内容，方便格式化以及输出。
```
class BooheeItem(scrapy.Item):
    name = scrapy.Field()
    value = scrapy.Field()
```
6.运行
```
scrapy crawl boohee
``
  
  
  
  
  
  
    
[1].https://virtualenv.pypa.io/en/stable/   
[2].https://doc.scrapy.org/en/latest/index.html

