from recent_posts_pipes import *
from substack_json_handler import *
import os
from time import sleep
import re
import chompjs

class ArchievedPostsCrawler(PostsCrawler):

    PATH = r"Files/"

    def __init__(self, name=None, codename=None, base_url=None, xpath_datetime=None, xpath_time=None, xpath_title=None, xpath_link=None, single_author=True, author=None, xpath_comments_amount=None, likes_amount=None, has_categories=False, xpath_post_content=None, **kwargs):
        super().__init__(name, codename, base_url, xpath_datetime, xpath_time, xpath_title, xpath_link, single_author, author, xpath_comments_amount, likes_amount, has_categories, **kwargs)
        self._xpath_post_content = xpath_post_content
        self._posts = []
        self._headers = ['date_time', 'title', 'link', 'author', 'comments_amount']
        self._dir = self.PATH+self._codename+"/"
        if isinstance(self._xpath_likes_amount, str):
            self._headers.append("likes_amount")
        if not os.path.isdir(self.PATH):
            os.mkdir(self.PATH)
        self._single_author = single_author


    def close(self, reason):
        sleep(30)
        self.write_posts_to_file(self._headers, self._posts)
            

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }
        # not sending an user-agent header causes 403 forbiden by server error
        yield scrapy.Request(url=self._url, headers=headers, callback=self.extract_archieved_links)
    
    def write_posts_to_file(self, headers, posts):
        with open(r'Files/'+self._codename+r'.csv', 'w', newline='') as csvfile:
            fieldnames = headers
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in posts:
                writer.writerow(row)
    
    def write_post_text_to_html(self, text):
        pass
        if not os.path.isdir(self._dir):
            os.mkdir(self._dir)
        if not os.path.isdir(self._dir+"HTMLs"):
            os.mkdir(self._dir+"HTMLs")
        with open(self._dir+"HTMLs/"+self._title[0].replace("/", "-").replace("\\", "-")+".html", "w") as file:
            html_initial = f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{self._title[0]}</title></head><body><h1>{self._title[0]}</h1>'
            file.write(html_initial)
            for line in text:
                file.write(line)
            html_ending = '</body></html>'
            file.write(html_ending)
    
    def write_post_text_to_txt(self, text):
        pass
        if not os.path.isdir(self._dir):
            os.mkdir(self._dir)
        if not os.path.isdir(self._dir+"TXTs/"):
            os.mkdir(self._dir+"TXTs/")
        with open(self._dir+"TXTs/"+self._title[0].replace("/", "-").replace("\\", "-")+".txt", "w") as file:
            file.write(self._title[0] + "\n")
            for line in text:
                file.write(line)
        
    def html_text_constructor(self, divs):
        text = []
        for p in divs.xpath('p'):
            text.append(p.get())
        return text
    
    def txt_text_constructor(self, divs):
        text = ""
        for p in divs.xpath('p'):
            text += re.sub("<[^>]*>", "",p.get().replace("</p>", "\n"))
        return text
    
    def extract_post(self, response):
        sleep(2)
        self._datetime = self.extract_part(response, self._xpath_datetime)
        self._title = self.extract_part(response, self._xpath_title)
        self._author = self._author if int(self._single_author) == 1 else self.extract_part(response, self._xpath_author)[0]
        if isinstance(self._xpath_author, str):
            self._author = self.extract_part(response, self._xpath_author)
        if isinstance(self._xpath_likes_amount, str):
            if ("substack" in self._url) and ("script" in self._xpath_likes_amount):
                javascript = response.xpath('//script[3]/text()').get()
                data = chompjs.parse_js_object(javascript)
                self._likes_amount = data["post"]["reactions"]["\u2764"]
            else:
                self._likes_amount = self.extract_part(response, self._xpath_likes_amount)
        if isinstance(self._xpath_comments_amount, str):
            self._comments_amount = self.extract_part(response, self._xpath_comments_amount)
            wrong_strings = ["print", "Facebook", "RSS", "Twitter"]
            self._comments_amount = [int(n.split(" ")[0].replace(",", "").replace(".", "")) for n in self._comments_amount if n.split(" ")[0] not in wrong_strings]
        row = {}
        row['date_time'] = self._datetime[0] 
        row['title'] = self._title[0] 
        row['author'] = self._author[0] if int(self._single_author) == 0 else self._author
        row['link'] = response.request.url
        if isinstance(self._xpath_comments_amount, str):
            row['comments_amount'] = self._comments_amount[0] if len(self._comments_amount) >= 1 else None
        if isinstance(self._xpath_likes_amount, str):
            row['likes_amount'] = self._likes_amount
        self._posts.append(row)
        if isinstance(self._xpath_post_content, str):
            self._post_content = response.xpath(self._xpath_post_content)
            self.write_post_text_to_html(self.html_text_constructor(self._post_content))
            self.write_post_text_to_txt(self.txt_text_constructor(self._post_content))

        
    def list_ssc_links(self, response):
        ssc_archive_link_xpath = "//a[@rel='bookmark']/@href"
        self._links = self.extract_part(response=response, xpath=ssc_archive_link_xpath)
        for href in self._links:
            yield scrapy.Request(href, self.extract_post)
    
    def list_additional_mr_links(self, response):
        mr_additional_links_xpath = "//h2[@class='entry-title']/a/@href"
        self._additional_links = self.extract_part(response=response, xpath=mr_additional_links_xpath)
        for href in self._additional_links:
            yield scrapy.Request(href, self.extract_post)
        
    def list_other_pages_of_mr_links(self, response):
        mr_other_pages_pages_xpath = "//a[@class='page-number page-numbers']/@href"
        self._other_pages_links = self.extract_part(response=response, xpath=mr_other_pages_pages_xpath)
        for href in self._other_pages_links:
            yield scrapy.Request(href, self.list_additional_mr_links)

    def list_initial_mr_links(self, response):
        mr_archive_link_xpath = "//ul/li[@class='child']/a/@href"
        self._links = self.extract_part(response=response, xpath=mr_archive_link_xpath)
        for href in self._links:
            yield scrapy.Request(href, self.list_other_pages_of_mr_links)
            yield scrapy.Request(href, self.extract_post)

    def extract_archieved_links(self, response):
        if self._codename == "ACT":
            self._links = request_links_in_json_from_substack(domain = "astralcodexten", link_path = "canonical_url")
            for href in self._links:
                yield scrapy.Request(href, self.extract_post)
        if self._codename == "AK":
            self._links = request_links_in_json_from_substack(domain = "arnoldkling", link_path = "canonical_url")
            for href in self._links:
                yield scrapy.Request(href, self.extract_post)
        if self._codename == "SSC":
            yield scrapy.Request("https://slatestarcodex.com/archives/", self.list_ssc_links)
        if self._codename == "MR":
            yield scrapy.Request("https://marginalrevolution.com/date-archives", self.list_initial_mr_links)


if __name__ == '__main__':
    with open('Python_pipes/xpaths_archieved_posts.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner()
        for row in reader:
            r = runner.crawl(ArchievedPostsCrawler, 
                            url=row["base_url"],  
                            codename=row["codename"], 
                            base_url=row["base_url"], 
                            xpath_datetime=row["datetime"],
                            xpath_time=row["time"], 
                            xpath_title=row["title"], 
                            single_author=row["single_author"], 
                            author=row["author"], 
                            likes_amount=row["likes_amount"],
                            xpath_comments_amount=row["comments_amount"], 
                            xpath_post_content=row["content"]
                            )
        r.addBoth(lambda _: reactor.stop())
        reactor.run()
            