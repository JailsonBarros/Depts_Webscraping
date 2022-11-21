import scrapy

list_dep = []

class DeputadasSpider(scrapy.Spider):
    name = 'links_deputadas'
    start_urls = [f'https://www.camara.leg.br/deputados/quem-sao/resultado?search=&partido=&uf=&legislatura=56&sexo=F&pagina={i}' for i in range(1,5)]

    def parse(self, response):

        filename = f'links_deputadas.html'

        for i in response.xpath("//h3[@class='lista-resultados__cabecalho']"):
            link = i.xpath('./a/@href').get()
            list_dep.append(link)
        
        # Salva o html da pagina
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        # Salva os links em txt
        file=open('lista_deputadas.txt','w')
        for items in list_dep:
            file.writelines(items+'\n')

        file.close()