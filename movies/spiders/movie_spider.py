'''
    movie_spider.py

    written by: Quan Zhou
    written on: December 24th, 2014

    A python script to pull movie reviews from www.rottentomatoes.com

'''

print(__doc__)


import scrapy                                                   

# movies.item is a class that you have to write
from movies.items import MoviesItem

# Library for crawling rules
from scrapy.contrib.spiders import CrawlSpider, Rule            
from scrapy.contrib.linkextractors import LinkExtractor         
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


class MovieSpider(CrawlSpider):
    name = "movie"                                      # Must be unique
    allowed_domains = ["www.rottentomatoes.com"]        # Restrict spiders to a certain domain
    start_urls = [
        "http://www.rottentomatoes.com/top/bestofrt/?year=2014",    # Where the first spider starts
    ]

    # See readme.md for more on these rules (note: callback is set on our function 'parse_movie')
    rules = (
        Rule(SgmlLinkExtractor(allow=('http:\/\/www\.rottentomatoes\.com\/m\/\w+\/$', ), ), follow=True),
        Rule(SgmlLinkExtractor(allow=('\/m\/\w+\/reviews\/$', )), callback='parse_movie', follow=True),
        Rule(SgmlLinkExtractor(allow=('\/m\/\w+\/reviews\/\?page=\d+$', )), callback='parse_movie', follow=True),
    )

    # This function scrapes information from a page
    def parse_movie(self, response):
        # Assume our xpaths only work on our target page
        try:
            title = response.xpath('//div[@id="content"]//h2/text()').extract()
            page  = response.xpath('//span[@class="pageInfo"]/text()').extract()[0]
        except:
            print "Error in URL: %s" % response.url
            return

        
        print 'Title: %s , %s' % (title, page)
        reviews = set()

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
            
        # Push the scraped data into the datastructure we've written
        item = MoviesItem()
        item['title'] = title
        item['reviews'] = list(reviews)
        item['page'] = page
        
        yield item

