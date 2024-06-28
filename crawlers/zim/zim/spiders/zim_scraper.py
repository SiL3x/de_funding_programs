import scrapy
import re
from bs4 import BeautifulSoup

class ZimScraperSpider(scrapy.Spider):
    name = "zim_scraper"
    allowed_domains = ["www.zim.de"]
    start_urls = [
        "https://www.zim.de/SiteGlobals/ZIM/Forms/Listen/Erfolgsbeispiele/erfolgsbeispiele_Formular.html?resourceId=512cb524-8e07-4f56-add0-7f9b08c54f49&input_=19feba07-48a0-49c8-b19b-7b4055f224fa&pageLocale=de&templateQueryStringListen=&cl2Categories_Typ_name=&cl2Categories_Typ_name.GROUP=1&cl2Categories_TechnologieAnwendungsbereich_name=&cl2Categories_TechnologieAnwendungsbereich_name.GROUP=1&cl2Categories_Laender=&cl2Categories_Laender.GROUP=1&selectSort=&selectSort.GROUP=1#form-512cb524-8e07-4f56-add0-7f9b08c54f49"
    ]
    quotechar = "'"
    

    def parse(self, response):
        # get success stories
        programs = response.css("a.card-link-overlay::attr(href)").getall()
        print(programs)

        for program in programs:
            req = scrapy.Request(program, callback=self.sub_parse)
            yield req

        # process next result page
        next_page = response.css("a.pagination-link::attr(href)")[-1].get()

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def sub_parse(self, response):
        #print("\n", response.css(".title").get())
        program_type = str.split(BeautifulSoup(response.css(".document-info-item").getall()[0], 'html.parser').get_text(), "Förderansatz:")[1].strip()
        program_area = str.split(BeautifulSoup(response.css(".document-info-item").getall()[1], 'html.parser').get_text(), "Technologie:")[1].strip()
        program_region = str.split(BeautifulSoup(response.css(".document-info-item").getall()[2], 'html.parser').get_text(), "Bundesland:")[1].strip()
        program_description = BeautifulSoup(response.css(".rich-text.publication-text").get(), 'html.parser').get_text().strip()
        program_pdf = [response.css("a.link::attr(href)").get()]

        yield {
            "name": BeautifulSoup(response.css(".title").get(), 'html.parser').get_text().strip(),
            "type": program_type,  # [Projekt oder Program]
            "program": "",  # [Program Name, wenn Projekt]
            "program_link": "",
            "partner": "",
            "project_id": "",
            "runtime": "",  # TODO: parse to datatype date
            "start": "",  # [Start des Programs/Projekt]  # TODO: dito 
            "end": "",  # TODO: dito 
            "description": program_description,
            "region": program_region,
            "topics": program_area,
            "keywords": "",
            "contact": "",
            "approach": "",
            "eligible": "Unternehmen, KMU",
            "pdf_links": program_pdf,  # Liste
            "other_links": "",  # Liste
            "managing_organization": "Zentrale Innovation Mittelstand (ZIM)",
            "amount": "",
            "funding_provider": "BMWK",
            "funding_reciever": ""
        }
