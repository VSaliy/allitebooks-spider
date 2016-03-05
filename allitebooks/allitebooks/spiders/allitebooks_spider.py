# -*- coding:utf-8 -*-

import scrapy
from ..items import BookItem
from urlparse import urljoin

base_url = "http://www.allitebooks.com"


class AllITEBooksSpider(scrapy.Spider):
    name = "allitebooks"
    start_urls = [base_url]

    def parse(self, response):
        pages = int(response.xpath('//div[@class="pagination clearfix"]/a[last()]/text()').extract()[0])
        for i in xrange(pages):
            url = urljoin(base_url, "/page/{}".format(str(i+1)))
            yield scrapy.Request(url, callback=self.parse_pagination)

    def parse_pagination(self, response):
        book_urls = response.xpath("//h2/a/@href").extract()
        for book_url in book_urls:
            yield scrapy.Request(book_url, callback=self.parse_book_page)

    def parse_book_page(self, response):
        book = BookItem()
        book['name'] = response.xpath('//h1[@class="single-title"]/text()').extract()[0]
        book['auth'] = response.xpath('//div[@class="book-detail"]//dd[1]/a/text()').extract()[0]
        book['isbn'] = response.xpath('//div[@class="book-detail"]//dd[2]/text()').extract()[0]
        book['image'] = response.xpath('//div[@class="entry-body-thumbnail hover-thumb"]//img/@src').extract()[0]
        book['description'] = "".join(response.xpath('//div[@class="entry-content"]/p/text()').extract())
        book['pdf_url'] = response.xpath('//span[@class="download-links"][1]/a/@href').extract()[0]
        yield book
