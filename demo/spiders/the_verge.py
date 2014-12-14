from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from demo.items import DemoItem
class TheVerge(CrawlSpider):
    name = "the_verge"
    allowed_domains = ["www.theverge.com"]
    start_urls = ["http://www.theverge.com/reviews/%d" % d for d in range(1, 6)]
    rules = [Rule(SgmlLinkExtractor(allow=['reviews', 'review'], deny=[]), 'parse_page', follow=True)]

    def parse_page(self, response):
        l = ReviewLoader(item=extract_item(HtmlXPathSelector(response), response.url), response=response)
        return l.load_item()

def extract_item(hxs, url):
    item = DemoItem()
    item['url'] = url
    try:
        item['title'] = hxs.select("//head//title/text()").extract()[0]
    except IndexError:
        item['title'] = ''
    try:
        item['author'] = hxs.select("//li[@class='author']//a/text()").extract()[0]
    except IndexError:
        item['author'] = ''
    try:
        item['numberComments'] = \
        hxs.xpath("//header[@class='p-entry-header']//a[@class='p-entry-header__comments']//text()").extract()[0]
    except IndexError:
        item['numberComments'] = ''
    return item

class ReviewLoader(ItemLoader):
    default_input_processor = MapCompose(unicode.strip)
    default_output_processor = TakeFirst()
