import scrapy

from .utils.clean_data import CleanData

class InfoDeputadosSpider(scrapy.Spider):
    name = 'data_deputados'

    def start_requests(self):

        deps_file = open("lista_deputados.txt", "r")

        deps_urls = deps_file.read().splitlines()

        for url in deps_urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):

        cleaner = CleanData(response)

        #Raspagem

        name = response.xpath("//ul[@class='informacoes-deputado']/li[1]/text()").get()
        gender = "M" # << 
        birth_date = response.xpath("//ul[@class='informacoes-deputado']/li[5]/text()").get()
        if birth_date == None:
            birth_date = response.xpath("//ul[@class='informacoes-deputado']/li[2]/text()").get()

        presence_plenary_list = response.xpath("//li[@class='list-table__item'][1]//dd[@class='list-table__definition-description']/text()").extract()
        presence_plenary_list = cleaner.number_days(presence_plenary_list)

        presence_commission_list = response.xpath("//li[@class='list-table__item'][2]//dd[@class='list-table__definition-description']/text()").extract()
        presence_commission_list = cleaner.number_days(presence_commission_list)

        name_months_par = response.xpath("//table[@id='gastomensalcotaparlamentar']/tbody/tr/td[1]/text()").extract()
        value_months_par = response.xpath("//table[@id='gastomensalcotaparlamentar']/tbody/tr/td[2]/text()").extract()
        months_par = cleaner.monthly_expenses(name_months_par, value_months_par)
        total_expenses_par = round(sum(months_par.values()), 2)

        name_months_cab = response.xpath("//table[@id='gastomensalverbagabinete']/tbody/tr/td[1]/text()").extract()
        value_months_cab = response.xpath("//table[@id='gastomensalverbagabinete']/tbody/tr/td[2]/text()").extract()
        months_cab = cleaner.monthly_expenses(name_months_cab, value_months_cab)
        total_expenses_cab = round(sum(months_cab.values()), 2)

        salary = response.xpath("//a[@class='beneficio__info']/text()").get()
        salary = float(salary.split("\n")[1].replace(".", "").replace(",", ".").strip())

        trips = response.xpath("//div[@class='beneficio beneficio__viagens']//a[@class='beneficio__info']/text()").get()
        if (trips == None):
            trips = 0

        #Organização dos dados

        dep_data = {
            'nome': name,
            'genero': gender,
            'presenca_plenario': presence_plenary_list[0],
            'ausencia_plenario': presence_plenary_list[1],
            'ausencia_justificada_plenario': presence_plenary_list[2],
            'presença_comissao': presence_commission_list[0],
            'ausencia_comissao': presence_commission_list[1],
            'ausencia_justificada_comissao': presence_commission_list[2],
            'data_nascimento': birth_date,
            'gasto_total_par': total_expenses_par,
            'gasto_jan_par': months_par['jan'],
            'gasto_fev_par': months_par['fev'],
            'gasto_mar_par': months_par['mar'],
            'gasto_abr_par': months_par['abr'],
            'gasto_mai_par': months_par['mai'],
            'gasto_jun_par': months_par['jun'],
            'gasto_jul_par': months_par['jul'],
            'gasto_ago_par': months_par['ago'],
            'gasto_set_par': months_par['set'],
            'gasto_out_par': months_par['out'],
            'gasto_nov_par': months_par['nov'],
            'gasto_dez_par': months_par['dez'],
            'gasto_total_gab': total_expenses_cab,
            'gasto_jan_gab': months_cab['jan'],
            'gasto_fev_gab': months_cab['fev'],
            'gasto_mar_gab': months_cab['mar'],
            'gasto_abr_gab': months_cab['abr'],
            'gasto_mai_gab': months_cab['mai'],
            'gasto_jun_gab': months_cab['jun'],
            'gasto_jul_gab': months_cab['jul'],
            'gasto_ago_gab': months_cab['ago'],
            'gasto_set_gab': months_cab['set'],
            'gasto_out_gab': months_cab['out'],
            'gasto_nov_gab': months_cab['nov'],
            'gasto_dez_gab': months_cab['dez'],
            'salario_bruto': salary,
            'quant_viagem': trips
        }

        yield dep_data