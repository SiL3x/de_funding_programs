import scrapy


class WaldScraperSpider(scrapy.Spider):
    name = "wald_scraper"
    allowed_domains = ["www.waldklimafonds.de"]
    start_urls = ["https://www.waldklimafonds.de/projekte/projektdatenbank"]
    quotechar = "'"

    def parse(self, response):
        # get projects
        projects = response.css("a.details-link::attr(href)").getall()

        for project in projects:
            req = scrapy.Request(response.urljoin(project), callback=self.sub_parse)
            yield req

    def sub_parse(self, response):
        project_name = response.css(".large-9 > div:nth-child(4) > h2:nth-child(1)::text").get()
        program_partner = response.css("div.detail:nth-child(1) > div:nth-child(2)::text").getall()
        project_id = response.css("div.detail:nth-child(3) > div:nth-child(2)::text").getall()
        project_start = response.css("div.detail:nth-child(4) > div:nth-child(2)::text").get()
        project_end = response.css("div.detail:nth-child(5) > div:nth-child(2)::text").get()
        descrition = response.css("div.detail:nth-child(6) > div:nth-child(2)::text").getall()

        yield {
            "name": project_name,
            "type": "Projekt",  
            "program": "waldklimafonds", 
            "program_link": "https://torfersatz.fnr.de/",
            "partner": program_partner,
            "project_id": project_id,
            "runtime": "",  # TODO: parse to datatype date
            "start": project_start,  # [Start des Programs/Projekt]  # TODO: dito 
            "end": project_end,  # TODO: dito 
            "description": descrition,
            "region": "",
            "topics": "",
            "keywords": "",
            "contact": "",
            "approach": "",
            "eligible": "",
            "pdf_links": [""],
            "other_links": [""], 
            "managing_organization": "Fachagentur für Nachwachsende Rohstoffe",
            "amount": "",
            "funding_provider": "BMEL",
            "funding_reciever": ""
            }
