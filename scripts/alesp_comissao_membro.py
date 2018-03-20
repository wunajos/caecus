import xml.etree.ElementTree as ET
import pandas as pd
import requests

url = 'http://www.al.sp.gov.br/repositorioDados/processo_legislativo/comissoes_membros.xml'
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
dataset = dataset[['SiglaComissao', 
                   'IdComissao', 
                   'NomeMembro', 
                   'IdMembro', 
                   'Papel', 
                   'IdPapel', 
                   'Efetivo', 
                   'DataInicio',
                   'DataFim']]
dataset = dataset.rename(columns={
    'SiglaComissao': 'sigla_comissao', 
    'IdComissao': 'id_comissao', 
    'NomeMembro': 'nome_membro', 
    'IdMembro': 'id_membro', 
    'Papel': 'papel', 
    'IdPapel': 'id_papel', 
    'Efetivo': 'efetivo', 
    'DataInicio': 'data_inicio', 
    'DataFim': 'data_fim'
})
dataset.to_csv('alesp_comissoes_membros.csv', 
               encoding = 'utf-8', 
               sep = ';', index = False)
