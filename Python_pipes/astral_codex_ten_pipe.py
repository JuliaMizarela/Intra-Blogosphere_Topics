"""
A pipe to flow data (titles, dates and number of comments and likes) of recent posts from Astral Codex Ten site to txt files.
"""

import scrapy
from scrapy.crawler import CrawlerProcess


class AstralCodexRecentPosts(scrapy.Spider):

    name = "astral_codex_ten_recent_posts_spider"

    def start_requests(self):
        url = "https://astralcodexten.substack.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }
        # not sending an user-agent header causes 403 forbiden by server error
        yield scrapy.Request(url=url, headers=headers, callback=self.extract_parts)

    def extract_parts(self, response):
        xpath_title = './a[contains(@class, "post-preview-title")]/text()'
        xpath_datetime = '//time/@datetime'
        xpath_comments_number = '//td[@class="post-meta-item icon"]/a/text()'
        xpath_likes_number = '//a[@class="like-button"]/text()'
        parts_xpaths = [xpath_title, xpath_datetime, xpath_comments_number, xpath_likes_number]
        parts = [self.extract_part(response, xpath) for xpath in parts_xpaths]
        parts_files = [
            r"../Files/astral_recent_titles.txt",
            r"../Files/astral_recent_datetimes.txt",
            r"../Files/astral_recent_comments_number.txt",
            r"../Files/astral_recent_likes_number.txt",
        ]
        _ = [
            self.write_recent_parts_to_file(parts[i], parts_files[i])
            for i in range(len(parts_xpaths))
        ]

    def extract_part(self, response, xpath):
        xpath_post = '//div[@class="post-preview-content"]'
        # Se você achou que nunca ia precisar de um ordered-set... (é um dicionário sem chaves, mas potato potato)
        part = [*dict.fromkeys(response.xpath(xpath_post).xpath(xpath).extract())]
        return part

    def write_recent_parts_to_file(self, part, file_name):
        with open(file_name, "w", encoding="UTF-8") as txt:
            for entry in part:
                txt.write(entry + "\n")


process = CrawlerProcess()
process.crawl(AstralCodexRecentPosts)
process.start()
