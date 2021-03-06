# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from news.items import NewsItem
class NewsPipeline(object):
	def open_spider(self, spider):
		f = open('res.csv', 'wb')
		exporter = CsvItemExporter(f)
		exporter.start_exporting()
		self.exporter=exporter
	def close_spider(self, spider):
		self.exporter.finish_exporting()
	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item