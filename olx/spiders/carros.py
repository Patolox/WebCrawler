import scrapy

class CarrosSpider(scrapy.Spider):

    name = 'carros'
    allowed_domains = ['pe.olx.com.br']
    start_urls = ['http://pe.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/']

    # def __init__(self, stats):
    #     super(CarrosSpider, self).__init__()
    #     self.stats = stats

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(crawler.stats)

    def parse(self, response):
        # self.stats.inc_value('count')
        # CarrosSpider.crawler.stats.inc_value('count')
        
        ul = response.xpath('//*[@id="content"]/div/div[2]/div[9]/ul/li')

        for li in ul:
            item = li.xpath('.//a/div/div[2]/div/div/h2/text()').extract_first()
            href = li.xpath('.//a/@href').extract_first()
            if item is not None:
                yield scrapy.Request(url= href, callback=self.parse_detail)
        
        next_page = response.xpath('//*[@id="content"]/div/div[2]/div[12]/ul/li[last()-1]/a/@href').extract_first()

        # if CarrosSpider.crawler.stats.get_value('count') < 4:
            
        yield scrapy.Request(url=next_page, callback=self.parse)
                
    def parse_detail(self, response):
        divs = response.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div[25]/div/div[4]/div')
        valor = response.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div[6]/div/div/h2/text()').extract_first()

        info = {}
        
        for div in divs:
            appnd = div.xpath('.//div/div[2]/a/text()').extract_first()
            name = div.xpath('.//div/div[2]/span/text()').extract_first()
            
            if appnd is not None:
                info.update({'%s' % name : appnd})
            else:
                appnd = div.xpath('.//div/div[2]/span[2]/text()').extract_first()
                info.update({'%s' % name : appnd})

        info.update({'preco':valor})
            
        yield{
            'info':info
        }