# Crawler de projetos de leis do Estado de São Paulo
# Criado por Rodolfo Viana, em 22.dez.2017

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as req

ano = input('Digite um ano: ')
url = 'https://www.al.sp.gov.br/alesp/projetos/?tipo=1&ano={}'.format(year)
html = req(url)
site = html.read()
html.close()

pagina = bs(site, 'html.parser')