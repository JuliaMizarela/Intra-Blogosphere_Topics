"""
A pipe to flow data (titles, authors, dates and tags) of recent posts from Marginal Revolution site to txt files.
"""

import scrapy
from scrapy.crawler import CrawlerProcess


class MarginalRecentPosts(scrapy.Spider):

    name = "marginal_revolution_recent_posts_spider"

    def start_requests(self):
        url = "https://marginalrevolution.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }
        # not sending an user-agent header causes 403 forbiden by server error
        yield scrapy.Request(url=url, headers=headers, callback=self.extract_parts)

    def extract_parts(self, response):
        xpath_title = '//h2[@class="entry-title"]/a/text()'
        xpath_link= '//h2[@class="entry-title"]/a'
        xpath_datetime = "//time/@datetime"
        xpath_author = '//*[@class="author"]/a/text()'
        xpath_tags = '//ul[@class="entry-tags"]/li[@class="tag"]/a/text()'
        parts_xpaths = [xpath_title, xpath_author, xpath_link, xpath_datetime, xpath_tags]
        parts = [self.extract_part(response, xpath) for xpath in parts_xpaths]
        parts_files = [
            "marginal_recent_titles.txt",
            "marginal_recent_authors.txt",
            "marginal_recent_links.txt",
            "marginal_recent_datetimes.txt",
            "marginal_recent_tags.txt",
        ]
        _ = [
            self.write_recent_parts_to_file(parts[i], parts_files[i])
            for i in range(len(parts_xpaths))
        ]

    def extract_part(self, response, xpath):
        xpath_post = "//article[1]"
        # An ordered-set... 
        part = [*dict.fromkeys(response.xpath(xpath_post).xpath(xpath).extract())]
        # ...is just a dictionary without keys, but tomato tomato
        return part

    def write_recent_parts_to_file(self, part, file_name):
        with open(file_name, "w", encoding="UTF-8") as txt:
            for entry in part:
                txt.write(entry + "\n")


process = CrawlerProcess()
process.crawl(MarginalRecentPosts)
process.start()
