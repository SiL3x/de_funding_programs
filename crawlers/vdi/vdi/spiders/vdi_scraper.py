import scrapy


class VdiScraperSpider(scrapy.Spider):
    name = "vdi_scraper"
    allowed_domains = ["www.vditz.de"]
    start_urls = ["https://www.vditz.de/service/foerderbekanntmachungen"]

    def parse(self, response):
        pass
