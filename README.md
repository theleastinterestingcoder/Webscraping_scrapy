Webscraping_scrapy
==========

How to crawl through a website using Scrapy spiders

Introduction 
------

Scrapy (http://scrapy.org/) is a powerful tool that will collect information across different webpages. Scrapy starts with one webpage and does a depth first search of all the links based on a set of rules. In this example, we'll start on rotten tomatoes home page, and we'll limit our crawling to the first 20 pages of a movie. 


If you want to learn more, check out their FAQ in this link here: 


Installing Scrapy
------

If you have pip (which I strongly recommend that you install for these tutorials), just type:

```
http://scrapy.org/
```

If things break in the middle of your installation, don't panic! You might need to install some basic dependencies (such as xcode). 


Scraping all the reviews
------

The structure of `rottentomatoes.com` page looks like this:
![Structure of the domain we want to scrape](https://github.com/theleastinterestingcoder/Webscraping_scrapy/blob/master/resources/outline.jpg)

We want to grab everything the blue box: the review given, and whether the author thought the movie was fresh or rotten. 
