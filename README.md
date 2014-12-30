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


