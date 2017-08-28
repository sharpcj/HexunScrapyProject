# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class HexunprojectPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="localhost", user="root", passwd="aaa123", db="hexun")
        self.cursor = self.conn.cursor()
        self.conn.set_charset('utf8')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def process_item(self, item, spider):
        for j in range(0, len(item['name'])):
            name = item['name'][j]
            url = item['url'][j]
            hits = item['hits'][j]
            comment = item['comment'][j]
            sql = "insert into myhexun (name,url,hits,comment) VALUES ('" + name + "','" + url + "','" + hits + "','" + comment + "')"
            try:
                # 执行sql语句
                self.cursor.execute(sql)
                # 提交到数据库执行
                self.conn.commit()
            except pymysql.Error as e:
                # 如果发生错误则回滚
                self.conn.rollback()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
