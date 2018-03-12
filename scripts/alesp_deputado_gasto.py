import xml.etree.ElementTree as ET
import pandas as pd
import requests

url = 'http://www.al.sp.gov.br/repositorioDados/deputados/despesas_gabinetes.xml'
xml_data = requests.get(url).content

class XML2DataFrame:

    def __init__(self, xml_data):
        self.root = ET.XML(xml_data)

    def parse_root(self, root):
        return [self.parse_element(child) for child in iter(root)]

    def parse_element(self, element, parsed=None):
        if parsed is None:
            parsed = dict()
        for key in element.keys():
            parsed[key] = element.attrib.get(key)
        if element.text:
            parsed[element.tag] = element.text
        for child in list(element):
            self.parse_element(child, parsed)
        return parsed

    def process_data(self):
        structure_data = self.parse_root(self.root)
        return pd.DataFrame(structure_data)

xml2df = XML2DataFrame(xml_data)
dataset = xml2df.process_data()
dataset = dataset[['Deputado', 
                   'Matricula', 
                   'Ano', 
                   'Mes', 
                   'Tipo', 
                   'Fornecedor', 
                   'CNPJ',
                   'Valor']]
dataset = dataset.rename(columns={
    'Deputado': 'deputado',
    'Matricula': 'matricula',
    'Ano': 'ano',
    'Mes': 'mes',
    'Tipo': 'tipo',
    'Fornecedor': 'fornecedor',
    'CNPJ': 'cnpj', 
    'Valor': 'valor'
})
dataset.to_csv('alesp_deputados_gastos.csv', 
               encoding = 'utf-8', 
               sep = ';', 
               index = False)
