import re

import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps = response.css('section#numerical-index td a::attr(href)')
        for num in range(0, len(all_peps), 2):
            yield response.follow(all_peps[num], callback=self.parse_pep)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_pep(self, response):
        head = response.css('section#pep-content h1 ::text').get()
        num, title = re.split(r' – ', head, maxsplit=1)
        status = response.css('dt:contains("Status") + dd abbr::text').get()
        data = {
            'number': num.replace('PEP ', ''),
            'name': title,
            'status': status,
        }

        yield PepParseItem(data)
