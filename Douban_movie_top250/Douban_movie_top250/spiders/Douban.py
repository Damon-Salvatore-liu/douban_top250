import scrapy
from scrapy import Request
from Douban_movie_top250.items import DoubanMovieTop250Item
from scrapy.linkextractors import LinkExtractor


class DoubanSpider(scrapy.Spider):
    name = 'Douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    def start_requests(self):
        for i in range(10):
            url = f'https://movie.douban.com/top250?start={25 * i}&filter='
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        le = LinkExtractor(restrict_css='div.pic a')
        for link in le.extract_links(response):
            yield Request(link.url, callback=self.parse_movie)

    def parse_movie(self, response):
        item = DoubanMovieTop250Item()
        sel = response.css('div#wrapper')
        item['name'] = sel.xpath(
            ".//div[@id='content']/h1/span[1]/text()").extract_first()
        yield item
