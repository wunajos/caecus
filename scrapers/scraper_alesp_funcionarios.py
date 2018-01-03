# -*- coding: utf-8 -*-
"""
Crawler de funcionários da Assembleia Legislativa do Estado de São Paulo
Criado em 2 de janeiro de 2018, às 22:06:26
@author: rodolfoviana
"""

import urllib.request
import xml.etree.cElementTree as et
import pandas as pd

req = urllib.request.urlopen('http://www.al.sp.gov.br/repositorioDados/administracao/funcionarios_lotacoes.xml')


def getvalueofnode(node):
    return node.text if node is not None else None


parsed_xml = et.parse(req)
dfcols = ['data_inicio', 'data_fim', 'id_cargo',
          'cargo', 'nome', 'id_regime', 'regime']

df_xml = pd.DataFrame(columns=dfcols)

for node in parsed_xml.getroot():
    data_inicio = node.find('DataInicio')
    data_fim = node.find('DataFim')
    id_cargo = node.find('IdCargo')
    cargo = node.find('NomeCargo')
    nome = node.find('NomeFuncionario')
    id_regime = node.find('IdRegime')
    regime = node.find('NomeRegime')

    df_xml = df_xml.append(
            pd.Series([getvalueofnode(data_inicio),
                       getvalueofnode(data_fim),
                       getvalueofnode(id_cargo),
                       getvalueofnode(cargo),
                       getvalueofnode(nome),
                       getvalueofnode(id_regime),
                       getvalueofnode(regime)], index=dfcols),
            ignore_index=True)

#   print(df_xml)

df_xml.to_csv('resultado.csv', sep=';', encoding='utf8')

# ESTRUTURA DO XML
# <CargoFuncionario> Raiz
#       <DataInicio> Data início do cargo do funcionário - date
#       <DataFim> Data fim do cargo do funcionário - date
#       <IdCargo> Identificador único do cargo - integer
#       <NomeCargo> Nome do cargo - string
#       <NomeFuncionario> Nome do Funcionário - string
#       <IdRegime> Identificador único do regime da lotação/cargo - integer
#       <NomeRegime> Nome do regime da lotação/cargo - string
