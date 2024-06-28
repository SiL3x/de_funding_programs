import scrapy

from selenium import webdriver


class NowScraperSpider(scrapy.Spider):
    name = "now_scraper"
    allowed_domains = ["www.now-gmbh.de"]
    start_urls = ["https://www.now-gmbh.de/foerderung/foerderfinder/"]

    def __init__(self):
        self.driver = webdriver.Firefox()
        
        self.programs = {
            "BAF": "Bodenstrom an Flughäfen",
            "MKS": "Mobilitäts- und Kraftstoffstrategie",
            "NIP": "Wasserstoff und Brennstoffzelle",
            "RK": "Regenerative Kraftstoffe",
            "EXI": "Exportinitiative Umweltschutz",
            "EM": "Elektromobilität",
            "LIS": "Ladesäuleninfrastruktur",
            "ZUG": "Alternative Antriebe im Schienenverkehr",
            "BUS": "Busse mit alternative Antrieben",
            "LKW": "Klimafreundliche Nutzfahrzeuge"
            }

    def parse(self, response):
        self.driver.get(start_urls[0])
        

        # load all projects
        xpath('//button[text()="Mehr laden"]')

        while True:
            try:
                next = self.driver.find_element_by_xpath('//button[text()="Mehr laden"]')
                next.click()
