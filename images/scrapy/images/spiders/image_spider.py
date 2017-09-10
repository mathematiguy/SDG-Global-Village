# -*- coding: utf-8 -*-
import scrapy
import pandas as pd

import os
import hashlib

from images.items import ImagesItem
from scrapy.pipelines.images import ImagesPipeline

def preprocess_data():
	data_path = "../../data/"
	images_path = "../full/"
	image_data = pd.read_csv(data_path + "search_results.csv")

	print(image_data.head())
	image_data = (image_data
	    .sort_values('index')
	    .groupby('query_name')
	    .head()
	    .sort_values(['country', 'query_name', 'index'])
	    [~image_data.downloaded])

	return image_data

class ImageSpiderSpider(scrapy.Spider):
    name = 'image_spider'

    def start_requests(self):
		image_data = preprocess_data()
		image_urls = list(image_data.link)

		item = ImagesItem()
		for image_url in image_urls:
		    yield scrapy.Request(
		    	url = image_url, callback = self.parse, 
		    	meta = {'item': item})

    def parse(self, response):
		yield {'image_urls': [response.url]}