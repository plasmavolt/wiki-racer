import scrapy


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Measure_(mathematics)"]

    def parse(self, response):
        for link in response.xpath('//p/a/@href').getall():
            yield {
                'link': link
            }
