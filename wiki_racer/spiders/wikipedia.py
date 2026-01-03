import scrapy
from collections import deque

from scrapy.exceptions import DropItem, CloseSpider

class WikipediaSpider(scrapy.Spider):
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 10,
        'DEPTH_PRIORITY': 1,
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
    }
    name = "wikipedia"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Measure_(mathematics)"]

    def parse(self, response):
        links = response.xpath('//p/a/@href').getall()
        for link in links:
            yield {
                'link': link
            }
            if link == "/wiki/Mathematics":
                raise CloseSpider('found!')
        
        
        next_page = response.urljoin(links[0])
        yield scrapy.Request(next_page, callback=self.parse)
