# -*- coding: utf-8 -*-
import scrapy


class SpiderDatasusSpider(scrapy.Spider):
    name = 'spider_datasus'
    allowed_domains = ['datasus.gov.br']
    start_urls = ['http://datasus.gov.br/']
    
    def __init__(self, *args, **kwargs):
        super(SpiderDatasusSpider).__init__(*args, **kwargs)
        self.args = kwargs

    def parse(self, response):
        pass
