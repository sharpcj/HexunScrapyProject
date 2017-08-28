# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.request
from hexunproject.items import HexunprojectItem
from scrapy.http import Request


class MyhexunspdSpider(scrapy.Spider):
    name = 'myhexunspd'
    allowed_domains = ['hexun.com']
    uid = "19940007"

    def start_requests(self):
        yield Request("http://" + str(self.uid) + ".blog.hexun.com/p1/default.html",
                      headers={
                          'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"})

    def parse(self, response):
        item = HexunprojectItem()
        item['name'] = response.xpath("//span[@class = 'ArticleTitleText']/a/text()").extract()
        item['url'] = response.xpath("//span[@class = 'ArticleTitleText']/a/@href").extract()

        pat1 = '<script type="text/javascript" src="http://click.tool.hexun.com/.*?">'
        temp_url = re.compile(pat1).findall(str(response.body))[0]
        pat11 = 'http://.*?">'
        hc_url = re.compile(pat11).findall(temp_url)[0]
        hc_url = str(hc_url[0:-2])
        header2 = ("User-Agent",
                   "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36")
        opener = urllib.request.build_opener()
        opener.addheaders = [header2]
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(hc_url).read()
        pat2 = "click\d*?','(\d*?)'"
        pat3 = "comment\d*?','(\d*?)'"
        item["hits"] = re.compile(pat2).findall(str(data))
        item["comment"] = re.compile(pat3).findall(str(data))

        yield item

        totalpage = (response.xpath("//div[@class='PageSkip_1']/a[last()-1]/text()").extract())[0]
        print("----------------------------")
        print("---------------" + totalpage)
        for i in range(2, int(totalpage) + 1):
            nexturl = "http://" + str(self.uid) + ".blog.hexun.com/p" + str(i) + "/default.html"
            yield Request(nexturl, callback=self.parse,
                          headers={
                              'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"}
                          )
