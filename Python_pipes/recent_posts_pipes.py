"""
A pipe to flow data (titles, dates and number of comments and likes) of posts from Marginal Revolution and Astral Codex Ten.
"""
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import csv


class PostsCrawler(scrapy.Spider):
    name = 'posts_crawler'

    def __init__(self, name=None, codename=None, base_url=None, xpath_datetime=None, xpath_time=None, xpath_title=None, xpath_link=None, single_author=True, author=None, xpath_comments_amount=None, likes_amount=None, has_categories=False, **kwargs):
        super().__init__(name, **kwargs)
        if isinstance(codename, str):
            self._codename = codename
        if isinstance(base_url, str):
            self._url = base_url
        if isinstance(xpath_datetime, str):
            self._xpath_datetime = xpath_datetime
        if bool(int(xpath_time)):
            self._xpath_time = xpath_time
        if not bool(int(xpath_time)):
            self._xpath_time = None
        if isinstance(xpath_title, str):
            self._xpath_title = xpath_title
        if isinstance(xpath_link, str):
            self._xpath_link = xpath_link
        else: 
            self._xpath_link = None
        if bool(int(single_author)):
            self._author = author
            self._xpath_author = None
        if not bool(int(single_author)):
            self._xpath_author = author
        if isinstance(xpath_comments_amount, str):
            self._xpath_comments_amount = xpath_comments_amount
        else:
            self._xpath_comments_amount = None
        if isinstance(likes_amount, str) and len(likes_amount) > 2:
            self._xpath_likes_amount = likes_amount
        else:
            self._xpath_likes_amount = None
        if has_categories and isinstance(has_categories, bool):
            pass
            """TODO create a post<->catergories relationship list"""
        self.headers = ['date_time', 'title', 'author']
        self.rows = []

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }
        # not sending an user-agent header causes 403 forbiden by server error
        yield scrapy.Request(url=self._url, headers=headers, callback=self.extract_recent_posts)


    def extract_part(self, response, xpath): 
        return response.xpath(xpath).extract()

    def write_recent_parts_to_file(self, headers, rows):
        with open(r'Files/'+self._codename+r'_test.csv', 'w', newline='') as csvfile:
            fieldnames = headers
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
    
    def extract_recent_posts(self, response):
        self._datetimes = self.extract_part(response, self._xpath_datetime)
        if isinstance(self._xpath_time, str):
            self._times = self.extract_part(response, self._xpath_time)
            self._datetimes = [f"{self._datetimes[i]} {self._times[i]}" for i in range(len(self._datetimes))]
        self._titles = self.extract_part(response, self._xpath_title)
        if isinstance(self._xpath_author, str):
            self._authors = self.extract_part(response, self._xpath_author)
        if isinstance(self._xpath_link, str):
            self._links = self.extract_part(response, self._xpath_link)
            self.headers.append('link')
        if isinstance(self._xpath_comments_amount, str):
            self._comments_amounts = self.extract_part(response, self._xpath_comments_amount)
            wrong_strings = ["print", "Facebook", "RSS", "Twitter"]
            self._comments_amounts = [int(n.split(" ")[0].replace(",", "").replace(".", "")) for n in self._comments_amounts if n.split(" ")[0] not in wrong_strings]
            self.headers.append('comments_amount')
        if isinstance(self._xpath_likes_amount, str):
            self._likes_amounts = self.extract_part(response, self._xpath_likes_amount)
            self.headers.append('likes_amount')
        for i in range(len(self._datetimes)):
            row = {}
            row['date_time'] = self._datetimes[i]
            row['title'] = self._titles[i]
            if isinstance(self._xpath_author, str):
                row['author'] = self._authors[i]
            else:
                row['author'] = self._author
            if isinstance(self._xpath_link, str):
                row['link'] = self._links[i]
            if isinstance(self._xpath_comments_amount, str):
                row['comments_amount'] = int(self._comments_amounts[i])
            if isinstance(self._xpath_likes_amount, str):
                row['likes_amount'] = int(self._likes_amounts[i])
            self.rows.append(row)
        self.write_recent_parts_to_file(self.headers, self.rows)

if __name__ == '__main__':
    with open('Python_pipes/xpaths_recent_posts.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner()
        for row in reader:
                r = runner.crawl(PostsCrawler, 
                                url=row["base_url"],  
                                codename=row["codename"], 
                                base_url=row["base_url"], 
                                xpath_datetime=row["datetime"],
                                xpath_time=row["time"], 
                                xpath_title=row["title"], 
                                xpath_link=row["link"], 
                                single_author=row["single_author"], 
                                author=row["author"], 
                                xpath_comments_amount=row["comments_amount"], 
                                likes_amount=row["likes_amount"])
        r.addBoth(lambda _: reactor.stop())
        reactor.run()
            
        
        