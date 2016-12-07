# -*- coding: utf-8 -*-
import scrapy
import MySQLdb


class GubaSpider(scrapy.Spider):
    name = "guba"
    allowed_domains = ["guba.eastmoney.com"]

    filter_author = [
        u'北京时代资讯',
        u'财经评论',
        u'东方财富网',
    ]

    filter_post = [
        '研报',
        '公告'
    ]

    host = 'http://guba.eastmoney.com'

    def start_requests(self):
        conn, cursor = self.connect_user_database()
        for item in self.get_all_stock(conn, cursor):
            yield scrapy.Request(
                    'http://guba.eastmoney.com/list,%s.html' % item,
                    callback=self.parse)

    def parse(self, response):
        element_list = []
        element_list = response.xpath('.//div[@class="articleh"]') + response.xpath('.//div[@class="articleh odd"]')
        print len(element_list)

        for element in element_list:
            author = '' . join(
                    element.xpath('.//span[@class="l4"]/a/text()').extract())
            if not author:
                author = '' . join(
                        element.xpath('.//span[@class="l4"]/span/text()').extract())

            if author in self.filter_author:
                continue

            try:
                hinfo = '' . join(element.xpath('.//span[@class="l3"]/em[@class="hinfo"]/text').extract())
                if hinfo in self.filter_post:
                    continue
            except:
                pass

            next_url = '' . join(element.xpath('.//span[@class="l3"]/a/@href').extract())
            next_url = self.host + next_url
            print next_url




    def get_all_stock(self, conn, cursor):
        select_sql = 'select stock_code from im2_company_core limit 2'
        cursor.execute(select_sql)
        for item in cursor.fetchall():
            yield item[0]

    def connect_user_database(self):
        conn = MySQLdb.connect(
                'localhost',
                'root',
                'yxs',
                'company_core',
                charset='utf8')
        cursor = conn.cursor()

        return conn, cursor
