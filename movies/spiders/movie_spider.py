import scrapy
from movies.items import MoviesItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


class MovieSpider(CrawlSpider):
    name = "movie"
    allowed_domains = ["www.rottentomatoes.com"]
    start_urls = [
        "http://www.rottentomatoes.com/top/bestofrt/?year=2014",
#        "http://www.rottentomatoes.com/top/bestofrt/?year=2013",
#        "http://www.rottentomatoes.com/top/bestofrt/?year=2012",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('http:\/\/www\.rottentomatoes\.com\/m\/\w+\/$', ), ), follow=True),
        Rule(SgmlLinkExtractor(allow=('\/m\/\w+\/reviews\/$', )), callback='parse_movie', follow=True),
        Rule(SgmlLinkExtractor(allow=('\/m\/\w+\/reviews\/\?page=\d+$', )), callback='parse_movie', follow=True),
    )

    def parse_movie(self, response):
        try:
            title = response.xpath('//div[@id="content"]//h2/text()').extract()
            page = response.xpath('//span[@class="pageInfo"]/text()').extract()[0]
        except:
            print "Error in URL: %s" % response.url
            return

        reviews = set()

        print 'Title: %s , %s' % (title, page)

        # When we hit the appropriate page, try to scrape the review from each table row
        for sel in response.xpath('//div[@id="reviews"]//table//tr'):
            # The content of the review
            review = sel.xpath('.//p/text()').extract()[0]

            # Is this review positive or negative?
            if sel.xpath('.//td//div[contains(@class,"fresh")]'):
                rating = 'fresh'
            elif sel.xpath('.//td//div[contains(@class,"rotten")]'):
                rating = 'rotten'

            reviews.add((rating, review))
            

            

        item = MoviesItem()
        item['title'] = title
        item['reviews'] = list(reviews)
        item['page'] = page
        yield item

