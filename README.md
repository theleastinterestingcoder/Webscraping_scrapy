Webscraping_scrapy
==========

How to crawl through a website using Scrapy spiders

Introduction 
------

Scrapy (http://scrapy.org/) is a powerful tool that will collect information across different webpages. Scrapy starts with one webpage and unleashes `spiders` that preform depth first searches of the target website. In this example, we'll scrape rotten tomatoes and grab all the reviews written about the top movies of 2014. 

What Scrapy is Doing Under the Hood
-------

A domain consists of a series of nodes (webpages) and links between these nodes (links): 

![Structure of the domain we want to scrape](https://github.com/theleastinterestingcoder/Webscraping_scrapy/blob/master/resources/img_web2db.gif)

When scraping a webpage, there are a couple of challenges that scrapy helps us solve:

* Keeping track of the webpages (nodes) we've already visited.
* Keeping track of the links (edges) we've haven't tried yet.
* Restricting which links/nodes we want to search.
* Crawling and scraping webpages in parallel - this involves facilitating communication between all of our spiders.
* Defining behavoir for handling links. Ex: We want to follow, but not scrape intermediate pages. 
* Defining the search behavoir. Ex: we want to do a BFS instead of a DFS (default). 
* And much, much more. 

As you'll see, Scrapy does a good job addressing these problems, but it doesn't solve everything. 


Installing Scrapy
------

If you have pip (which I strongly recommend that you install for these tutorials), just type:

```
pip install scrapy
```

If things break in the middle of your installation, don't panic! You might need to install some basic dependencies (such as xcode). 



Scraping all the reviews
------

The structure of `rottentomatoes.com` page looks like this:
![Structure of the domain we want to scrape](https://github.com/theleastinterestingcoder/Webscraping_scrapy/blob/master/resources/outline.jpg)

For each review, we want to know:
* the review given
* is the movie fresh or rotten?

To do that, we'll need `spiders` that will do wander through all the links. More specifically, we want to:

* Start at the initial URL `http://www.rottentomatoes.com/top/bestofrt/?year=2014`

* Venture to the landing page of each movie Ex: `http://www.rottentomatoes.com/m/boyhood/`

* Look and then scrape for all the reviews. Ex: `http://www.rottentomatoes.com/m/boyhood/reviews/`

* If the movie has more than one page, follow and scrape those. Ex: `http://www.rottentomatoes.com/m/boyhood/reviews/?page=2`

Executing Scrapy
--------

To run scrapy out of the box, type in:

```
scrapy crawl movie -o foo.json
```

This tells scrapy to crawl the internet using the spiders that have been named `movie` and collect the parsed information into the output file `foo.json`. You should start seeing the progress of the spiders on the screen (here's the first couple of lines):
```

    movie_spider.py

    written by: Quan Zhou
    written on: December 24th, 2014

    A python script to pull movie reviews from www.rottentomatoes.com


2014-12-31 20:45:56-0500 [scrapy] INFO: Scrapy 0.24.4 started (bot: movies)
2014-12-31 20:45:56-0500 [scrapy] INFO: Optional features available: ssl, http11, django
2014-12-31 20:45:56-0500 [scrapy] INFO: Overridden settings: {'NEWSPIDER_MODULE': 'movies.spiders', 'FEED_FORMAT': 'json', 'SPIDER_MODULES': ['movies.spiders'], 'FEED_URI': 'foo.json', 'BOT_NAME': 'movies'}
2014-12-31 20:45:56-0500 [scrapy] INFO: Enabled extensions: FeedExporter, LogStats, TelnetConsole, CloseSpider, WebService, CoreStats, SpiderState
2014-12-31 20:45:56-0500 [scrapy] INFO: Enabled downloader middlewares: HttpAuthMiddleware, DownloadTimeoutMiddleware, UserAgentMiddleware, RetryMiddleware, DefaultHeadersMiddleware, MetaRefreshMiddleware, HttpCompressionMiddleware, RedirectMiddleware, CookiesMiddleware, ChunkedTransferMiddleware, DownloaderStats
2014-12-31 20:45:56-0500 [scrapy] INFO: Enabled spider middlewares: HttpErrorMiddleware, OffsiteMiddleware, RefererMiddleware, UrlLengthMiddleware, DepthMiddleware
2014-12-31 20:45:56-0500 [scrapy] INFO: Enabled item pipelines: 
2014-12-31 20:45:56-0500 [movie] INFO: Spider opened
2014-12-31 20:45:56-0500 [movie] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2014-12-31 20:45:56-0500 [scrapy] DEBUG: Telnet console listening on 127.0.0.1:6023
2014-12-31 20:45:56-0500 [scrapy] DEBUG: Web service listening on 127.0.0.1:6080
2014-12-31 20:45:57-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/top/bestofrt/?year=2014> (referer: None)
2014-12-31 20:45:59-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/12_oclock_boys_2013/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:45:59-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/mistaken_for_strangers/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:45:59-0500 [movie] DEBUG: Filtered duplicate request: <GET http://www.rottentomatoes.com/m/12_oclock_boys_2013/> - no more duplicates will be shown (see DUPEFILTER_DEBUG to show all duplicates)
2014-12-31 20:45:59-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/obvious_child/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:45:59-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/the_skeleton_twins/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:45:59-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/art_and_craft/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:45:59-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/tims_vermeer_2014/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:45:59-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/to_be_takei/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:45:59-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/top_five/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:45:59-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/big_hero_6/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:46:00-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/le_week_end/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:46:00-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/the_guest_2014/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:46:00-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/omar/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:46:00-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/a_most_violent_year/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:46:00-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/chef_2014/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:46:01-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/diplomatie/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:46:01-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/dear_white_people/> (referer: http://www.rottentomatoes.com/top/bestofrt/?year=2014)
2014-12-31 20:46:02-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/12_oclock_boys_2013/reviews/> (referer: http://www.rottentomatoes.com/m/12_oclock_boys_2013/)
2014-12-31 20:46:02-0500 [movie] INFO: Closing spider (shutdown)
2014-12-31 20:46:03-0500 [movie] DEBUG: Crawled (200) <GET http://www.rottentomatoes.com/m/reach_me/> (referer: http://www.rottentomatoes.com/m/12_oclock_boys_2013/)
Title: [u"12 O'clock Boys Reviews"] , Page 1 of 3
2014-12-31 20:46:03-0500 [movie] DEBUG: Scraped from <200 http://www.rottentomatoes.com/m/12_oclock_boys_2013/reviews/>
    {'page': u'Page 1 of 3',
     'reviews': [('fresh',
                  u'An exciting, beautifully shot look at a subculture through the eyes of one of its most devoted admirers.'),
                 ('rotten',
                  u'[It] spectacularizes black criminality for white middle-class viewers, the primary audience for the festivals and art houses where this film will have its career.'),
                 ('fresh',
                  u"That Nathan is able to cover so much ground in a mere 76 minutes makes 12 O'Clock Boys all the more remarkable and essential."),
                 ('fresh',
                  u"Lotfy Nathan's hand-held camerawork, combined with a snappy hip-hop soundtrack, gives the documentary a sense of immediacy."),
                 ('fresh',
                  u'One of the more unique looks at the Other America to come down the line in recent years'),
                 ('fresh',
                  u'Documentary filmmaker Lotfy Nathan explores the outlaw appeal of an inner-city Baltimore dirt-bike gang through the eyes of a 13-year-old wannabe member named Pug.'),
                 ('fresh',
                  u"The result is evocative and compelling, even if it doesn't offer much context or socioeconomic insight into its broader subject."),
                 ('fresh',
                  u"It's the rare film that gets deep into low income inner city life and zeroes in on what motivates those whom society tends to forget."),
                 ('fresh',
                  u"It's important to remember that not every day is a joy ride. 12 O'Clock Boys is also a portrait of a family."),
                 ('fresh',

```

Here are some important points:
* Each spider crawls through all the links as a Depth First Search Order. Each spider will traverse the freshest link avaible. 
* Since there are multiple spiders, You'll note that there's no real order or pattern that data is generated.
* `Crawled (200): <GET ...>` means that a spider successfully located and crawled the URL with a GET request. The `200` is the response code for a successful request. `404` is the response code for a `page not found` error, and `403` is the response code for non-adequate permissions. 



Fundamental Limitations
---------

* Some domains (such as Facebook) might not be happy about you scraping their data. If they see your IP accessing their domain too frequently, they might ban your IP address. 
* Scraping is (relatively) slow. It's important to be specific about how you want to scrape information. Most large domains would take hours (or even days) for you to exhaustively crawl through all of the links. 
* Getting the data is only half the battle. Most of the time, you'll also need to spend a lot of time cleaning and validating the information that you've fetched. 

What To Do Next
----------
The best way to learn is to try scrapy out yourself! Try the following:
* Scrape one page with scrapy's own tutorial: `http://doc.scrapy.org/en/latest/intro/tutorial.html`
* Learn how to write a `CrawlSpider` in its namesake section near the bottom of this page: http://doc.scrapy.org/en/latest/topics/spiders.html
* Scrape and create your own dataset! Hint: there are a lot of cool things you can do with Twitter. 


