import scrapy
import re
from bs4 import BeautifulSoup


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["www.foerderdatenbank.de"]
    start_urls = ["https://www.foerderdatenbank.de/SiteGlobals/FDB/Forms/Suche/Expertensuche_Formular.html?resourceId=c4b4dbf3-4c29-4e70-9465-1f1783a8f117&input_=bd101467-e52a-4850-931d-5e2a691629e5&pageLocale=de&filterCategories=FundingProgram&filterCategories.GROUP=1&templateQueryString=&submit=Suchen"]
    quotechar = "'"
    n=0
    
    def parse(self, response):
        # get funding programs
        programs = response.css(".card.card--horizontal.card--fundingprogram")

        for program in programs:
            program_url = program.css("a::attr(href)").extract_first()
            req = scrapy.Request(response.urljoin(program_url), callback=self.sub_parse)
            req.meta["name"] = program.css("a::text").extract_first()
            yield req

        # process next result page
        next_page = response.css("a.forward::attr(href)").get()

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def sub_parse(self, response):
        name = BeautifulSoup(response.css(".title").get(), 'html.parser').get_text()
        values = response.css("dd::text").getall()
        keys = [x.replace(" ", "") for x in response.css("dt::text").getall()]
        infos = dict(zip(keys, values))  # infos zu förderart, wer, ansprechpartner etc
        text_html = response.css(".content--main").get()
        text = BeautifulSoup(text_html, 'html.parser').get_text()
        
        yield {
            "name": name,
            "type": infos["Förderart:"],  # [Projekt oder Program]
            "program": "",# [Program Name, wenn Projekt]
            "program_link": "",
            "partner": "",
            "project_id": "",
            "runtime": "",  # TODO: parse to datatype date
            "start": "",  # [Start des Programs/Projekt]  # TODO: dito 
            "end": "",  # TODO: dito 
            "description": text,
            "region": infos["Fördergebiet:"],
            "topics": infos["Förderbereich:"],
            "keywords": "",
            "contact": infos["Ansprechpunkt:"],
            "approach": "",
            "eligible": infos["Förderberechtigte:"],
            "pdf_links": [""],  # Liste
            "other_links": [""],  # Liste
            "managing_organization": "",
            "amount": "",
            "funding_provider": infos["Fördergeber:"] if "Fördergeber" in keys else "",
            "funding_reciever": ""
        }

