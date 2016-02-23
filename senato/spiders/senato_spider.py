# -*- coding: utf-8 -*-

import scrapy

from senato.items import Amendment


class SenatoSpider(scrapy.Spider):

    """TODO."""

    name = 'senato'
    allowed_domains = ['senato.it']
    start_urls = [
        'http://www.senato.it/leg/17/BGT/Schede/Ddliter/testi/46051_testi.htm'
    ]

    def parse(self, response):
        """TODO."""
        for href in response.xpath('//dl[@class="emendamenti"]/dt/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_amendment)

    def parse_amendment(self, response):
        """TODO."""
        ps = response.xpath('//div[@id="testo"]/p')

        amendment = Amendment()
        amendment['_id'] = self._parse_id(ps[0])
        amendment['authors'] = self._parse_authors(ps[1])
        amendment['status'] = self._parse_status(ps[2])
        amendment['text'] = self._parse_text(ps[3:])

        yield amendment

    def _parse_id(self, p):
        """TODO."""
        return p.xpath('b/text()').extract()[0]

    def _parse_authors(self, p):
        """TODO."""
        return p.xpath('a/text()').extract()

    def _parse_status(self, p):
        """TODO."""
        try:
            status = p.xpath('b/text()').extract()[0]
        except IndexError:
            return 'PENDING'

        if status == 'Respinta':
            return 'REJECTED'
        elif status == 'Ritirato':
            return 'WITHDRAWN'
        else:
            return 'UNKNOWN'

    def _parse_text(self, ps):
        """TODO."""
        result = []

        for p in ps:
            try:
                result.append(p.xpath('text()').extract()[0].strip())
            except IndexError:
                pass

        return '\n'.join(result)
