# -*- coding: utf-8 -*-
"""
Crawler de despesas de gabinetes da Assembleia Legislativa do Estado de São Paulo
Criado em 8 de janeiro de 2018, às 00:49:56
@author: rodolfoviana
"""

import xml.etree.cElementTree as ET
import csv

tree = ET.parse('despesas_gabinetes.xml')
root = tree.getroot()

def get_node_text(tree, q):
    node = tree.find(q)
    if node is None:
        return ""
    return node.text

with open('resultado.csv', 'w', encoding='utf-8') as despesas:
    csvwriter = csv.writer(despesas, delimiter=';')
    cabecalhos = []
    count = 0
    for i in root.findall('despesa'):
	    dep = []
	    if count == 0:
		    deputado = i.find('Deputado').tag
		    cabecalhos.append(deputado)
		    matricula = i.find('Matricula').tag
		    cabecalhos.append(matricula)
		    ano = i.find('Ano').tag
		    cabecalhos.append(ano)
		    mes = i.find('Mes').tag
		    cabecalhos.append(mes)
		    tipo = i.find('Tipo').tag
		    cabecalhos.append(tipo)
		    cnpj = i.find('CNPJ').tag
		    cabecalhos.append(cnpj)
		    fornecedor = i.find('Fornecedor').tag
		    cabecalhos.append(fornecedor)
		    valor = i.find('Valor').tag
		    cabecalhos.append(valor)
		    csvwriter.writerow(cabecalhos)
		    count += 1

	    deputado = get_node_text(i, 'Deputado')
	    dep.append(deputado)
	    matricula = get_node_text(i, 'Matricula')
	    dep.append(matricula)
	    ano = get_node_text(i, 'Ano')
	    dep.append(ano)
	    mes = get_node_text(i, 'Mes')
	    dep.append(mes)
	    tipo = get_node_text(i, 'Tipo')
	    dep.append(tipo)
	    cnpj = get_node_text(i, 'CNPJ')
	    dep.append(cnpj)
	    fornecedor = get_node_text(i, 'Fornecedor')
	    dep.append(fornecedor)
	    valor = get_node_text(i, 'Valor')
	    dep.append(valor)
	    csvwriter.writerow(dep)
despesas.close()
