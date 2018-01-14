# -*- coding: utf-8 -*-
"""
Crawler de deputados na Assembleia Legislativa do Estado de São Paulo
Criado em 11 de janeiro de 2018, às 22:58:02
@author: rodolfoviana
"""

from __future__ import print_function
from xml.sax import ContentHandler, parse
import requests
import csv

arquivo = requests.get('https://www.al.sp.gov.br/repositorioDados/deputados/deputados.xml')

with open('deputados.xml','wb') as f:
    f.write(arquivo.content)

class Handler(ContentHandler):

    def __init__(self):
        ContentHandler.__init__(self)
        self.deputado = {}
        self.deputados = []
        self.current_field = None
        self.in_deputado = False
        self.indent = 0

    def startElement(self, name, attrs):
        print('{}Start element: {}'.format('\t' * self.indent, name))
        self.indent += 1
        if self.in_deputado:
            self.current_field = name
            self.deputado[name] = ''

        if name == 'Deputado':
            self.in_deputado = True

    def endElement(self, name):
        self.indent -= 1
        print('{}End element: {}'.format('\t' * self.indent, name))
        if name == 'Deputado':
            self.deputados.append(self.deputado)
            self.deputado = {}
            self.in_deputado = False
            self.current_field = None

    def characters(self, content):
        if content.strip():
            print('{}chars: {}'.format('\t' * self.indent, repr(content)))
        if self.in_deputado and self.current_field:
            self.deputado[self.current_field] += content


def gravar_deputados(writer, deputados):
    cabecalhos = ['IdDeputado', 'IdSPL', 'IdUA', 'Situacao',
                  'Andar', 'Aniversario', 'Email',
                  'Matricula', 'NomeParlamentar', 'PathFoto',
                  'PlacaVeiculo', 'Sala', 'Partido', 'Telefone']
    writer.writerow(cabecalhos)

    for deputado in deputados:
        writer.writerow([deputado.get(c, '').strip() for c in cabecalhos])


def main():

    handler = Handler()
    with open('deputados.xml', 'r', encoding='utf-8') as xml_file:
        parse(xml_file, handler)

    print('Encontrados {} deputados'.format(len(handler.deputados)))

    with open('deputados.csv', 'w', encoding='latin-1', newline='') as f_handle:
        writer = csv.writer(f_handle)
        gravar_deputados(writer, handler.deputados)


if __name__ == "__main__":
    main()
