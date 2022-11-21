import scrapy

list_dep = []

class DeputadosSpider(scrapy.Spider):
    name = 'links_deputados'
    start_urls = [f'https://www.camara.leg.br/deputados/quem-sao/resultado?search=&partido=&uf=&legislatura=56&sexo=M&pagina={i}' for i in range(1,9)]

    def parse(self, response):

        filename = f'links_deputados.html'

        for i in response.xpath("//h3[@class='lista-resultados__cabecalho']"):
            link = i.xpath('./a/@href').get()
            list_dep.append(link)
        
        # Salva o html da pagina
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        # Salva os links em txt
        file=open('lista_deputados.txt','w')
        for items in list_dep:
            file.writelines(items+'\n')

        file.close()