# -*- coding: utf-8 -*-
from scrapy import Item, Field


class DemoItem(Item):
    url = Field()
    author = Field()
    title = Field()
    numberComments = Field()
