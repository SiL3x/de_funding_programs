import scrapy


class BleScraperSpider(scrapy.Spider):
    name = "ble_scraper"
    allowed_domains = ["service.ble.de"]
    start_urls = ["https://service.ble.de/ptdb/index2.php?site_key=141"]
    quotechar = "'"

    def parse(self, response):
        # get programs
        programs = response.css("a.RichTextIntLink::attr(href)").getall()

        for program in programs:
            req = scrapy.Request(response.urljoin(program), callback=self.sub_parse)
            yield req

        # process next result page
        next_page = response.css("li.blaetterNaviNaechste > a::attr(href)").get()

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def sub_parse(self, response):
        infos = response.css("td, th").css("*::text").getall()

        pdf_links = response.css(".Publication::attr(href)").getall()
        pdf_links = [response.urljoin(x) for x in pdf_links]
        name = infos[infos.index("Titel:") + 1]
        description = infos[infos.index('Beschreibung\xa0(dt.):') + 1] if 'Beschreibung\xa0(dt.):' in infos else ""
        program_start = infos[infos.index("Beginn:\xa0") + 1] if "Beginn:\xa0" in infos else ""
        program_end = infos[infos.index("Ende:\xa0") + 1] if "Ende:\xa0" in infos else ""
        project_id = infos[infos.index("Förderkennzeichen:") + 1] if "Förderkennzeichen:" in infos else ""
        contact = "".join(infos[infos.index("Kontakt:") + 1:]) if "Kontakt:" in infos else ""
        institution = infos[infos.index("Ausf.\xa0Einrichtung:") + 1] if "Ausf.\xa0Einrichtung:" in infos else ""
        topics = infos[infos.index("Themenfelder:") + 1] if "Themenfelder:" in infos else ""
        program = infos[infos.index("Förderprogramme:") + 1] if "Förderprogramme:" in infos else ""
        keywords = infos[infos.index("Schlagworte:") + 1] if "Schlagworte:" in infos else ""

        yield {
            "name": name,
            "type": "",  # [Projekt oder Program]
            "program": program,# [Program Name, wenn Projekt]
            "program_link": "",
            "partner": institution,
            "project_id": project_id,
            "runtime": "",  # TODO: parse to datatype date
            "start": program_start,  # [Start des Programs/Projekt]  # TODO: dito 
            "end": program_end,  # TODO: dito 
            "description": description,
            "region": "",
            "topics": topics,
            "keywords": keywords,
            "contact": contact,
            "approach": "",
            "eligible": "",
            "pdf_links": pdf_links,  # Liste
            "other_links": [""],  # Liste
            "managing_organization": "BLE PT",
            "amount": "",
            "funding_provider": "BMEL",
            "funding_reciever": ""
        }            
