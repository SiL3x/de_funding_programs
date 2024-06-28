import scrapy
from bs4 import BeautifulSoup

class DlrScaperSpider(scrapy.Spider):
    name = "dlr_scaper"
    allowed_domains = ["projekttraeger.dlr.de"]
    start_urls = ["https://projekttraeger.dlr.de/de/foerderung/foerderangebote-und-programme"]
    delimiter = "|"
    quotechar = "'"

    def parse(self, response):
        # get programs
        programs = response.css("a.clickable-layer-full-size::attr(href)").getall()

        for program in programs:
            req = scrapy.Request(response.urljoin(program), callback=self.sub_parse)
            yield req

        next_page = response.css("li.pager__item:nth-child(7) > a:nth-child(1)::attr(href)").get()

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def sub_parse(self, response):
        name = response.css("h1::text").get()
        description = response.css(".field--name-field-content-text > div:nth-child(2)").get()
        description = BeautifulSoup(description, 'html.parser').get_text().strip()
        program_region = response.css(
            ".field--name-field-funding-region > div:nth-child(2) > div:nth-child(1)::text"
        ).get()
        program_status = response.css(
            ".field--name-field-funding-time-limitation > div:nth-child(2) > div:nth-child(1)::text"
        ).get().strip()
        submission_deadline = response.css(".datetime::text").get()
        program_runtime = response.css(".field--name-field-funding-duration > div:nth-child(2)::text").get()
        program_backer = response.css(
            "div.block:nth-child(5) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)::text"
        ).get()
        links = response.css(".further-reading-link::attr(href)").get()
        program_url = response.url

        yield {
            "name": name,
            "type": "Programm",  
            "program": name,
            "program_link": program_url,
            "partner": "",
            "project_id": "",
            "runtime": program_runtime,  # TODO: parse to datatype datetime
            "start": "",  # TODO: dito 
            "end": "",  # TODO: dito 
            "description": description,
            "region": program_region,
            "topics": "",
            "keywords": "",
            "contact": "",  # TODO: Parse from website
            "approach": "",
            "eligible": "",
            "pdf_links": [""],  # Liste
            "other_links": links,  
            "managing_organization": "DLR Projektträger",
            "amount": "",
            "funding_provider": program_backer,
            "funding_reciever": ""
            }
