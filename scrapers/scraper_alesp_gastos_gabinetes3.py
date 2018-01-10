# -*- coding: utf-8 -*-
"""
Crawler de despesas de gabinetes da Assembleia Legislativa do Estado de São Paulo
Criado em 8 de janeiro de 2018, às 00:49:56
@author: rodolfoviana
"""

from __future__ import print_function
from xml.sax import ContentHandler, parse
import requests
import xml.etree.cElementTree as ET
import csv

file = requests.get('http://www.al.sp.gov.br/repositorioDados/deputados/despesas_gabinetes.xml')

with open('despesas_gabinetes.xml','wb') as f:
	f.write(file.content)

class Handler(ContentHandler):

    def __init__(self):
        ContentHandler.__init__(self)
        self.despesa = {}
        self.despesas = []
        self.current_field = None
        self.in_despesa = False
        self.indent = 0

    def startElement(self, name, attrs):
        print('{}Start element: {}'.format('\t' * self.indent, name))
        self.indent += 1
        if self.in_despesa:
            self.current_field = name
            self.despesa[name] = ''

        if name == 'despesa':
            self.in_despesa = True

    def endElement(self, name):
        self.indent -= 1
        print('{}End element: {}'.format('\t' * self.indent, name))
        if name == 'despesa':
            self.despesas.append(self.despesa)
            self.despesa = {}
            self.in_despesa = False
            self.current_field = None

    def characters(self, content):
        if content.strip():
            print('{}chars: {}'.format('\t' * self.indent, repr(content)))
        if self.in_despesa and self.current_field:
            self.despesa[self.current_field] += content


def gravar_despesas(writer, despesas):
    cabecalhos = [
        'Deputado',
        'Matricula',
        'Ano',
        'Mes',
        'Tipo',
        'CNPJ',
        'Fornecedor',
        'Valor'
    ]
    writer.writerow(cabecalhos)

    for despesa in despesas:
        writer.writerow([despesa.get(c, '').strip() for c in cabecalhos])


def main():

    handler = Handler()
    with open('despesas_gabinetes.xml', 'r', encoding='utf-8') as xml_file:
        parse(xml_file, handler)

    print('Found {} despesas'.format(len(handler.despesas)))

    with open('despesas.csv', 'w', encoding='latin-1') as f_handle:
        writer = csv.writer(f_handle)
        gravar_despesas(writer, handler.despesas)


if __name__ == "__main__":
    main()

"""
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
"""