from typing import Iterable
import scrapy
import idna
import time
from scrapy_splash import SplashRequest


class BuildsSpider(scrapy.Spider):
    name = "builds"
    idn_domain = idna.encode('наш.дом.рф').decode('ascii')
    allowed_domains = [idn_domain]
    start_urls = [f'https://{idn_domain}/сервисы/каталог-новостроек/список-объектов/список?place=0-6']
    # allowed_domains = ["xn--80az8a.xn--d1aqf.xn--p1ai"]
    # start_urls = ["https://xn--80az8a.xn--d1aqf.xn--p1aiсервисы/каталог-новостроек/список-объектов/список?place=0-6"]

    # def parse(self, response):
    #     for builders in response.css("Newbuildings__NewBuildingList-sc-1bou0u4-14"):
    #         build = builders.css("a::attr(href)").get()
    #         yield response.follow(build, callback=self.parse_serves)


    # def parse_serves(self, response):
    #     for house in response.css("a::attr(href)").get():
    #         yield house
    script = """

    function(main, args)
        url = args.url
        assert(splash:go(url))
        return splash:html()
    end
    """

    def start_requests(self) :
        idn_domain = idna.encode('наш.дом.рф').decode('ascii')
        yield SplashRequest(url=f'https://{idn_domain}/сервисы/каталог-новостроек/список-объектов/список?place=0-6', callback=self.parse, endpoint='execute', args={
            'lua_source': self.script
        })

        
    def parse(self, response):
        page = response.meta["playwright_page"]
       
        print(111222333444555)
        time.sleep(3)
        for builders in response.css("div.NewBuildingItem__Wrapper-sc-o36w9y-0"):
            yield {
                "url_build" : builders.css("a::attr(href)").get(),
                "build_name" : builders.css("a.NewBuildingItem__MainTitle-sc-o36w9y-6::text").get()
            }

