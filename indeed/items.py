# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IndeedItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field()
    company_name = scrapy.Field()
    job_url = scrapy.Field()
    company_rating = scrapy.Field()
    location = scrapy.Field()
    remote = scrapy.Field()
    posted_date = scrapy.Field()
