import scrapy


class FoekatScraperSpider(scrapy.Spider):
    name = "foekat_scraper"
    allowed_domains = ["foerderportal.bund.de"]
    start_urls = ["https://foerderportal.bund.de/foekat/jsp/SucheAction.do?actionMode=searchmask"]
    quotechar = "'"

    def __init__(self):
        self.site_start_number = 11
        self.listrowpersite = 1000
    

    def parse(self, response):
        # submit form data
        return scrapy.FormRequest.from_response(
            response,
            formdata={"suche_schnellSuche": "*"},
            callback=self.parse_searchresults
        )

    def parse_searchresults(self, response):
        # get programs
        programs = list(set(
            response.css(response.urljoin("a.linkintextlook::attr(href)")).getall()
        ))
        
        for program in programs:
            req = scrapy.Request(response.urljoin(program), callback=self.sub_parse)
            yield req

        # process next result page
        next_page = response.css("#listnext > a:nth-child(5)::attr(href)").get()

        if next_page:
            print("\n\n+++ NEXT PAGE START:\t", self.site_start_number)
            
            formdata = {
                "suche.listrowfrom": str(self.site_start_number),
                "suche.listrowpersite": str(self.listrowpersite),
                "suche.orderby": "1",
                "suche.order": "asc"
                }
            self.site_start_number += self.listrowpersite
            yield scrapy.FormRequest.from_response(response,
                                        formdata=formdata,
                                            callback=self.parse_searchresults)

    def sub_parse(self, response):  # TODO: rework css paths
        name = response.css("div.detailAnsichtItem:nth-child(4) > div:nth-child(2)").get()
        program_backer = response.css("div.detailAnsichtItem:nth-child(6) > div:nth-child(2)::text").get()
        program_runtime = response.css("div.detailAnsichtItem:nth-child(8) > div:nth-child(2)::text").get()  
        program_recipient = response.css("div.detailAnsichtItem:nth-child(12) > div:nth-child(2)::text").get()
        program_region = response.css("div.detailAnsichtItem:nth-child(12) > div:nth-child(6)::text").get()
        program_amount = response.css("div.detailAnsichtItem:nth-child(5) > div:nth-child(2)::text").get()
        program_manager = response.css("div.detailAnsichtItem:nth-child(7) > div:nth-child(2)::text").get()
        program_institution = response.css("div.detailAnsichtItem:nth-child(13) > div:nth-child(2)::text").get()
        program_coop = response.css("div.detailAnsichtItem:nth-child(3) > div:nth-child(2)::text").get()
        program_topic = response.css("div.detailAnsichtItem:nth-child(9) > div:nth-child(2)::text").get()
        program_profile = response.css("div.detailAnsichtItem:nth-child(11) > div:nth-child(2)::text").get()
        program_id = response.css("div.detailAnsichtItem:nth-child(2) > div:nth-child(2)::text").get()
        
        yield {
            "name": name,
            "type": program_profile,  # [Projekt oder Program]
            "program": "",  # [Program Name, wenn Projekt]
            "program_link": "",
            "partner": program_institution,
            "project_id": program_id,
            "runtime": program_runtime, # TODO: parse to datatype date
            "start": "",  # [Start des Programs/Projekt]  # TODO: dito 
            "end": "",  # TODO: dito 
            "description": "",
            "region": program_region,
            "topics": program_topic,
            "keywords": "",
            "contact": "",
            "approach": "",
            "eligible": "",
            "pdf_links": "",  # Liste
            "other_links": "",  # Liste
            "managing_organization": program_manager,
            "amount": program_amount,
            "funding_provider": program_backer,
            "funding_reciever": program_recipient
        }
