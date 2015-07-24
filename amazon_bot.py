import scrapy
import urlparse
from tutorial.items import TutorialItem
from scrapy.selector import Selector
from scrapy.http import Request



class MySpider(scrapy.Spider):
    name = 'amazy'
    allowed_domains = ['amazon.in']
    start_urls = ['http://www.amazon.in/s/ref=sr_nr_n_1?fst=as%3Aoff&rh=n%3A1805560031%2Ck%3Amobiles&keywords=mobiles&ie=UTF8&qid=1437540979&rnid=3576079031']
    global flag;
    flag =0;    
    def parse(self, response):
  
        res_arr = response.xpath('//div[contains(@class,"s-item-container")]')
        for res in res_arr:
    
            item = TutorialItem()
            link_arr = res.xpath('.//div[contains(@class,"a-section a-spacing-none a-inline-block s-position-relative")]/a/@href').extract()
            # link = link_arr[0].extract()
            link =  str(link_arr[0]).encode('utf-8').strip()        
            item['link_from_am'] = link

            
            item['title'] = res.xpath(
                './/div[contains(@class,"a-row a-spacing-none")]/a/@title').extract()            

       	    if not item['title']:
            	item['title']="n/a"
            	flag = 1
            else:	
            	item['title'] = str(item['title'][0]).encode('utf-8').strip()	     

        	
            item['price_from_am'] = res.xpath(
                './/div[contains(@class,"a-row a-spacing-none")]/a/span[contains(@class,"a-size-base a-color-price s-price a-text-bold")]/text()').extract()

            if not item['price_from_am']:
            	item['price_from_am'] = "n/a"
            	
            else :	
            	item['price_from_am'] = float(item['price_from_am'][0].replace("Rs.","").replace("," , "").strip())
           

            request = scrapy.Request(link, callback=self.tech_details)
            print request            
            request.meta['item'] = item
		    			            
            yield request
            	          
        href = response.xpath('//a[@id="pagnNextLink"]/@href').extract()[0] #urlparse is for making absolute path(i.e. url) form relative path(i.e. href)
        url = urlparse.urljoin(response.url, href)
        yield scrapy.Request(url, callback=self.parse)


    def tech_details(self, response):
        flag=0
        item = response.meta["item"]        
        hxs = Selector(response)
       
       	item['image_src'] = hxs.xpath(
            ".//div[contains(@class,'imgTagWrapper')]/img/@src").extract()
        if not item['image_src']:
            item['image_src']="n/a"
            # flag = 1 
        else:
            item['image_src']=str(item['image_src'][0]).encode('utf-8').lower().strip()      

        item['color'] = hxs.xpath("//div[contains(@id,'prodDetails')]/div[contains(@class,'disclaim')]/strong/text()").extract()    
       	if item['color']:          
           item['color'] = str(item['color'][0]).encode('utf-8').lower().strip()	     
        else :
        	item['color'] = " "
				        	


        if item['price_from_am'] == "n/a" :
            item['price_from_am'] = hxs.xpath(
            ".//div[contains(@class,'a-section a-spacing-small a-spacing-top-small')]/span[contains(@class,'olp-padding-right')]/span[contains(@class,'a-color-price')]/text()").extract()
            item['price_from_am'] = float(item['price_from_am'][0].replace("Rs.","").replace("," , "").strip())


                  

        #Select Details Table      
        rows = hxs.xpath("//div[contains(@class,'pdTab')]/table/tbody/tr")

        color = rows.xpath("td[.=' Colour ']/following-sibling::td[1]/text()").extract()
        if color != "" : 
	        color = str(color[0]).encode('utf-8').lower().strip()	     	
	        item['color'] = color

   
        item['internal'] = rows.xpath("td[.='Memory Storage Capacity']/following-sibling::td[1]/text()").extract()
        if not item['internal']:
        	item['internal']="n/a"	 			
       	else :	
	        item['internal']=str(item['internal'][0]).encode('utf-8').strip()   
	        internal=str(item['internal']).split( )
	        if len(internal) == 2:
	            if internal[1] !="GB":
	                    item['internal']=float(internal[0]/1024)
	            else:
	                    item['internal']=float(internal[0])

		
		# item['color'] = rows.xpath("td[.=' Colour ']/following-sibling::td[1]/text()").extract()
		# item['color'] = str(item['color'][0]).encode('utf-8').lower().strip()	     
		# else :
		# 	flag = 1	



	if flag==1 :
            return flag
        
        return item     
            
            
 		# item['brand'] = rows.xpath("td[.='Brand']/following-sibling::td[1]/text()").extract()
            
		#item['ScreenSize'] = rows.xpath("td[.='Screen Size']/following-sibling::td[1]/text()").extract()	
	     
		#item['weight'] = rows.xpath("td[.='Item Weight']/following-sibling::td[1]/text()").extract()