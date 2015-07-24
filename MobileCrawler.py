__author__ = 'shruti'


# Crawler to crawl flipkart site to retrieve mobiles data


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
    name = "price_compare_spider"
    allow_domains = ["flipkart.com"]

    start_urls = ['http://www.flipkart.com/mobiles/pr?sid=tyy,4io&otracker=nmenu_quicklinks_All']

    rules = [
    Rule(LinkExtractor(allow=r'mobiles\/pr\?sid=tyy,4io&start=[0-9]'),
         callback='parse_list', follow=True)
    ]

    global flag
    flag =0 

    def parse_list(self, response):
        hxs = Selector(response)
        titles = hxs.select(
            "//div[contains(@class,'product-unit unit-4 browse-product new-design')]")
        items = []
        count1 = 0
        for title in titles:
            count1 = count1 + 1
            item = TutorialItem()
            item['title'] = title.select(
                ".//div[contains(@class,'pu-title')]/a/text()").extract()

            if not item['title']:
                item['title']="n/a"
            else:
                item['title']=str(item['title'][0]).encode('utf-8').strip()
            if item['title']== "n/a":
                flag = 1
            

            item['price_from_fk'] = title.select(
                ".//div[contains(@class,'pu-final')]/span/text()").extract()
            if not item['price_from_fk']:
                flag = 1
            else:
                item['price_from_fk']=float(item['price_from_fk'][0].replace("Rs.","").replace(",","").strip())


            item['link_from_fk'] = title.select(
                    ".//div[contains(@class,'pu-title')]/a/@href")[0].extract()
            if not item['link_from_fk']:
                item['link_from_fk'] = "n/a"
            else:
                item['link_from_fk'] = "http://www.flipkart.com" + item['link_from_fk']


            request = Request(
                item['link_from_fk'], callback=self.new_features)
            request.meta['item'] = item
            items.append(item)
            yield request

    def new_features(self,response):
        flag = 0
        item = response.meta["item"]
        hxs = Selector(response)

                            # item['image_src'] = hxs.select(
                            #     ".//div[contains(@class,'imgWrapper')]/img[1]/@data-zoomimage").extract()
                            # if not item['image_src']:
                            #     item['image_src']="n/a"
                            # else:
                            #     item['image_src']=item['image_src'][0]

        rows = hxs.xpath("//div[contains(@class,'productSpecs')]/table/tr")
      
        item['ram'] = rows.xpath("td[.='Memory']/following-sibling::td[1]/text()").extract()
        if not item['ram']:
            item['ram']="n/a"
        else:
            item['ram']=str(item['ram'][0]).encode('utf-8').strip()
            ram = item['ram'].split( )
            if (ram) :
                if ram[1] !="GB":
                    item['ram']=float(ram[0]/1024)
                else:
                    item['ram']=float(ram[0])

        if  item['ram'] == "n/a" :
            flag = 1               




        item['internal'] = rows.xpath("td[.='Internal']/following-sibling::td[1]/text()").extract()
        if not item['internal']:
            item['internal']="n/a"
        else:
            
            item['internal']=str(item['internal'][0]).encode('utf-8').strip()
            internal=item['internal'].split( )
            if len(internal) == 2:
                if internal[1] !="GB":
                    item['internal']=float(internal[0]/1024)
                else:
                    item['internal']=float(internal[0])

        if item['internal'] == "n/a":
            flag=1
                    

        item['brand'] = rows.xpath("td[.='Brand']/following-sibling::td[1]/text()").extract()
        if not item['brand']:
            item['brand']="n/a"
        else:
            item['brand']=str(item['brand'][0]).encode('utf-8').lower().strip()
        if item['brand'] == "n/a" :
            flag = 1    


        item['color'] = rows.xpath("td[.='Handset Color']/following-sibling::td[1]/text()").extract()
        if not item['color']:
            item['color']="n/a"
            flag = 1 
        else:
            
            item['color']=str(item['color'][0]).encode('utf-8').lower().strip()

        

        item['os'] = rows.xpath("td[.='OS']/following-sibling::td[1]/text()").extract()
        if not item['os']:
            item['os']="n/a"
        else:
            item['os']=str(item['os'][0]).encode('utf-8').strip()

        if flag==1 :
            return flag

        return item

