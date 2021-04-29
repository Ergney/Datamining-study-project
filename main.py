from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from autoruparce.spiders.auto import AutoSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule("autoruparce.settings")
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    crawler_proc.crawl(AutoSpider)
    crawler_proc.start()