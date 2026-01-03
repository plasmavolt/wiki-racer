# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem, CloseSpider
import json


class WikiRacerPipeline:
    
    itemlist = []
    
    def open_spider(self, spider):
        self.file = open("items.jsonl", "w")
        
    def close_spider(self, spider):
        self.file.close()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item).asdict()
        if item in self.itemlist:
            raise DropItem
        self.itemlist.append(item)
        
        line = json.dumps(adapter) + "\n"
        self.file.write(line)
        return item
