# -*- coding: utf-8 -*-
import scrapy
 
 
class DatasusSpider(scrapy.spiders.feed.CSVFeedSpider):
    name = 'datasus'
    allowed_domains = ['datasus.gov.br']
   
    def __init__(self, *args, **kwargs):
        super(DatasusSpider, self).__init__(*args, **kwargs)
        self.args = kwargs
   
    def start_requests(self):
        _formdata = {
            'Arquivos': 'hdsp1304.dbf',
            'Coluna': u'--Não-Ativa--'.encode('ISO-8859-1'),
            # 'formato': 'table',
            'formato': 'prn',
            'Incremento': u'Hipertensão'.encode('ISO-8859-1'),
            'Linha': u'Município'.encode('ISO-8859-1'),
            'mostre': 'Mostra',
            # 'pesqmes1': 'Digite+o+texto+e+ache+fácil',
            # 'pesqmes18': 'Digite+o+texto+e+ache+fácil',spiders/
            # 'pesqmes2': 'Digite+o+texto+e+ache+fácil',
            # 'pesqmes3': 'Digite+o+texto+e+ache+fácil',
            # 'pesqmes4': 'Digite+o+texto+e+ache+fácil',
            # 'pesqmes5': 'Digite+o+texto+e+ache+fácil',
            # 'pesqmes6': 'Digite+o+texto+e+ache+fácil',
            'SAcidente_V.Cereb': 'TODAS_AS_CATEGORIAS__',
            'SAmput_p/_Diabete': 'TODAS_AS_CATEGORIAS__',
            u'SDivisão_administ_estadual'.encode('ISO-8859-1'): 'TODAS_AS_CATEGORIAS__',
            u'SDoença_Renal'.encode('ISO-8859-1'): 'TODAS_AS_CATEGORIAS__',
            u'SFaixa_Etária'.encode('ISO-8859-1'): 'TODAS_AS_CATEGORIAS__',
            'SInfarto_Agu.Mioc': 'TODAS_AS_CATEGORIAS__',
            u'SMacrorregião_de_Saúde'.encode('ISO-8859-1'): 'TODAS_AS_CATEGORIAS__',
            u'SMicrorregião_IBGE'.encode('ISO-8859-1'): 'TODAS_AS_CATEGORIAS__',
            u'SMunicípio'.encode('ISO-8859-1'): 'TODAS_AS_CATEGORIAS__',
            'SOutras_Coronar': 'TODAS_AS_CATEGORIAS__',
            u'SPé_Diabético'.encode('ISO-8859-1'): 'TODAS_AS_CATEGORIAS__',
            u'SRegião_de_Saúde_(CIR)'.encode('ISO-8859-1'): 'TODAS_AS_CATEGORIAS__',
            u'SRegião_Metropolitana_-_RIDE'.encode('ISO-8859-1'): 'TODAS_AS_CATEGORIAS__',
            'SRisco': 'TODAS_AS_CATEGORIAS__',
            'SSedentarismo': 'TODAS_AS_CATEGORIAS__',
            'SSexo': 'TODAS_AS_CATEGORIAS__',
            'SSobrepeso': 'TODAS_AS_CATEGORIAS__',
            'STabagismo': 'TODAS_AS_CATEGORIAS__',
        }
        for _uf in self.args['uf'].split():
            yield scrapy.http.FormRequest('http://tabnet.datasus.gov.br/cgi/tabcgi.exe?hiperdia/cnv/hdSP.def',
                                          headers={
                                            'Host': 'tabnet.datasus.gov.br',
                                            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
                                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                            'Accept-Language': 'en-GB,en;q=0.5',
                                            'Accept-Encoding': 'gzip, deflate',
                                            # 'Referer': 'http://tabnet.datasus.gov.br/cgi/deftohtm.exe?hiperdia/cnv/hdSP.def',
                                            'Content-Type': 'application/x-www-form-urlencoded',
                                            # 'Content-Length': '1108',   
                                            'Connection': 'keep-alive',
                                            'Upgrade-Insecure-Requests': '1',
                                          },
                                          formdata=_formdata)
        #    yield scrapy.Request('http://tabnet.datasus.gov.br/cgi/deftohtm.exe?hiperdia/cnv/hd{}.def'.format(_uf))
 
    def parse(self, response):
        csv_content = response.css('div.testeira:nth-child(1) > pre:nth-child(7)::text').extract_first()
        print(csv_content)
        # csv_path = response.css('.botao_opcao a::attr(href)').extract_first()
        # csv_url = 'http://tabnet.datasus.gov.br{}'.format(csv_path)
        
        # return scrapy.Request(csv_url, callback=self.parse_csv)
    def parse_rows(self, response):
        """Receives a response and a dict (representing each row) with a key for
        each provided (or detected) header of the CSV file.  This spider also
        gives the opportunity to override adapt_response and
        process_results methods for pre and post-processing purposes.
        """

        for row in csviter(response, self.delimiter, self.headers, self.quotechar):
            ret = iterate_spider_output(self.parse_row(response, row))
            for result_item in self.process_results(response, ret):
                yield result_item
    
    # def parse_csv(self, response):
    #     response = self.adapt_response(response)
    #     return self.parse_rows(response)