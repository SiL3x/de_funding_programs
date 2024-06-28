import scrapy

from bs4 import BeautifulSoup


class BmfsScraperSpider(scrapy.Spider):
    name = "bmfs_scraper"
    allowed_domains = ["www.zukunft-der-wertschoepfung.de"]
    start_urls = ["https://www.zukunft-der-wertschoepfung.de/projekte/"]
    quotechar = "'"

    def parse(self, response):
        # get funding programs
        programs = response.css(".projekte__post--title a::attr(href)").getall()

        for program in programs:
            req = scrapy.Request(response.urljoin(program), callback=self.sub_parse)
            yield req

        # process next result page
        next_page = response.css(".next::attr(href)").get()

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
        
    def sub_parse(self, response):
        name = response.css(".default_content > h1:nth-child(2)::text").get()
        fundingprogram_name = response.css("p.mb-0 a::text").getall()
        fundingprogram_link = response.css("p.mb-0 a::attr(href)").get()
        project_runtime = "".join(response.css(".dates > span:nth-child(1)::text").getall())

        if fundingprogram_link:
            fundingprogram_link = response.urljoin(fundingprogram_link)
        
        program_runtime = "".join(
            str.split(BeautifulSoup(response.css(".dates").get(), 'html.parser').get_text(), "Laufzeit:")
        ).strip()
        program_link = response.css(".mt-3::attr(href)").get()
        program_description = BeautifulSoup(
            response.css(
                "div.js-accordion-item:nth-child(1) > div:nth-child(2) > div:nth-child(1)").get(), 'html.parser'
        ).get_text()
        program_partner = BeautifulSoup(
            response.css(
                "div.js-accordion-item:nth-child(2) > div:nth-child(2) > div:nth-child(1) > ul:nth-child(1)"
            ).get(), 'html.parser').get_text()
        
        yield {
            "name": name,
            "type": "Projekt",  # [Projekt oder Program]
            "program": fundingprogram_name,  # [Program Name, wenn Projekt]
            "program_link": fundingprogram_link,
            "partner": program_partner,
            "project_id": "",
            "runtime": project_runtime,  # TODO: parse to datatime 
            "start": "",  # [Start des Programs/Projekt]  # TODO: dito 
            "end": "",  # TODO: dito 
            "description": program_description,
            "region": "",
            "topics": "",
            "keywords": "",
            "contact": "",
            "approach": "",
            "eligible": "",
            "pdf_links": [""],  # Liste
            "other_links": [fundingprogram_link],  # Liste
            "managing_organization": "Projektträger Karlsruhe (PTKA)",
            "amount": "",
            "funding_provider": "BMFS",
            "funding_reciever": ""
            }
