# -*- coding: utf-8 -*-
"""
Crawler de despesas de gabinetes da Assembleia Legislativa do Estado de São Paulo
Criado em 8 de janeiro de 2018, às 00:49:56
@author: rodolfoviana
"""

import urllib.request
import xml.etree.cElementTree as ET
import pandas as pd

req = urllib.request.urlopen('http://www.al.sp.gov.br/repositorioDados/deputados/despesas_gabinetes.xml')


def getvalueofnode(node):
    return node.text if node is not None else None


parsed_xml = ET.parse(req)
dfcols = ['deputado', 'matricula', 'ano', 'mes', 'tipo', 'cnpj', 'fornecedor', 'valor']

df_xml = pd.DataFrame(columns=dfcols)

for node in parsed_xml.getroot():
    deputado = node.find('Deputado')
    matricula = node.find('Matricula')
    ano = node.find('Ano')
    mes = node.find('Mes')
    tipo = node.find('Tipo')
    cnpj = node.find('CNPJ')
    fornecedor = node.find('Fornecedor')
    valor = node.find('Valor')

    df_xml = df_xml.append(
    	    pd.Series([getvalueofnode(deputado), 
    		           getvalueofnode(matricula), 
    		           getvalueofnode(ano),
    		           getvalueofnode(mes),
    		           getvalueofnode(tipo),
    		           getvalueofnode(cnpj),
    		           getvalueofnode(fornecedor),
    		           getvalueofnode(valor)], index=dfcols),
            ignore_index=True)

df_xml.to_csv('gastos_gabinetes.csv', sep=';')
