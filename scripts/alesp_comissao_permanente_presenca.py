import xml.etree.ElementTree as ET
import pandas as pd
import requests

url = 'http://www.al.sp.gov.br/repositorioDados/processo_legislativo/comissoes_permanentes_presencas.xml'
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
dataset = dataset[['IdReuniao', 
                   'DataReuniao', 
                   'IdPauta',
                   'SiglaComissao',
                   'IdComissao',
                   'Deputado',
                   'IdDeputado']]
dataset = dataset.rename(columns={
    'IdReuniao': 'id_reuniao', 
    'DataReuniao': 'data_reuniao', 
    'IdPauta': 'id_pauta', 
    'SiglaComissao': 'sigla_comissao', 
    'IdComissao': 'id_comissao', 
    'Deputado': 'deputado', 
    'IdDeputado': 'id_deputado'
})
dataset.to_csv('alesp_comissoes_permanentes_presencas.csv', 
               encoding = 'utf-8', 
               sep = ';', index = False)
