__author__ = 'shruti'

# Crawler to crawl flipkart site to retrieve laptops data
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from tutorial.items import TutorialItem

import json
import string


class FlipkartSpider(CrawlSpider):
    name = "flipkart_spider"
    allow_domains = ["flipkart.com"]

    start_urls = ['http://www.flipkart.com/laptops/pr?sid=6bo,b5g']

    rules = [
    Rule(LinkExtractor(allow=r'laptops\/pr\?sid=6bo,b5g&start=[0-9]'),
         callback='parse_list', follow=True)
    ]

    def parse_list(self, response):
        hxs = Selector(response)
        titles = hxs.select(
            "//div[contains(@class,'product-unit unit-4 browse-product new-design')]")
        items = []
        count1 = 0
        for title in titles:
            count1 = count1 + 1
            item = TutorialItem()
            item['model'] = title.select(
                ".//div[contains(@class,'pu-title')]/a/text()").extract()

            if not item['model']: 
                item['model']="n/a"
            else:
                item['model']=str(item['model'][0]).encode('utf-8').strip()

                
            item['offer'] = title.select(
                ".//div[contains(@class,'pu-final')]/span/text()").extract()
            if not item['offer']: 
                item['offer']=0.00
            else:
                item['offer']=float(item['offer'][0].replace("Rs.","").replace(",","").strip())
                    
            item['image'] = title.select(
                ".//div[contains(@class,'pu-visual-section')]/a/img/@data-src")[0].extract()
            if not item['image']: 
                item['image']="n/a"
            else:
                item['image']=item['image'][0]
                    
            item['standard_url'] = title.select(
                    ".//div[contains(@class,'pu-title')]/a/@href")[0].extract()
            if not item['standard_url']:
                item['standard_url']="n/a"
            else:
                item['standard_url']= "http://www.flipkart.com" + item['standard_url']
                        
            
            request = Request(
                item['standard_url'], callback=self.new_features)
            request.meta['item'] = item
            items.append(item)
            yield request

    def new_features(self,response):
        item = response.meta["item"]
        hxs = Selector(response)
      
        rows = hxs.xpath("//div[contains(@class,'productSpecs')]/table/tr")

        item['included_software']=rows.xpath("td[.='Included Software']/following-sibling::td[1]/text()").extract()
        if not item['included_software']:
            item['included_software']="n/a"
        else:
            item['included_software']=str(item['included_software'][0]).encode('utf-8').strip()
            
        
        item['ram']=rows.xpath("td[.='System Memory']/following-sibling::td[1]/text()").extract()
        if not item['ram']: 
            item['ram']="n/a"
        else:
            item['ram']=str(item['ram'][0]).encode('utf-8').strip()
            ram=item['ram'].split( )
            if len(ram)==3:
                if ram[1] !="GB":
                    item['ram']=float(ram[0]/1024)
                else:
                    item['ram']=float(ram[0])

                item['ram_type']=ram[2]

        item['brand'] = rows.xpath("td[.='Brand']/following-sibling::td[1]/text()").extract()
        if not item['brand']: 
            item['brand']="n/a"
        else:
            item['brand']=str(item['brand'][0]).encode('utf-8').strip()
        
        item['part_number'] = rows.xpath("td[.='Part Number']/following-sibling::td[1]/text()").extract()
        if not item['part_number']: 
            item['part_number']="n/a"
        else:
            item['part_number']=str(item['part_number'][0]).encode('utf-8').strip()
        
        item['model_id'] = rows.xpath("td[.='Model ID']/following-sibling::td[1]/text()").extract()
        if not item['model_id']: 
            item['model_id']="n/a"
        else:
            item['model_id'] = str(item['model_id'][0]).encode('utf-8').strip() 
        
        return item
  
