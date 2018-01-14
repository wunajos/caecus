# -*- coding: utf-8 -*-
"""
Crawler de deputados na Assembleia Legislativa do Estado de São Paulo
Criado em 14 de janeiro de 2018, às 17:27:43
@author: rodolfoviana

--------------------------
| WIP - WORK IN PROGRESS |
--------------------------

Relatório em 14.jan, às 17h47:

Traceback (most recent call last):
  File "scraper_alesp_proposicoes.py", line 85, in <module>
    main()
  File "scraper_alesp_proposicoes.py", line 75, in main
    parse(xml_file, handler)
  File "C:\ProgramData\Anaconda3\lib\xml\sax\__init__.py", line 33, in parse
    parser.parse(source)
  File "C:\ProgramData\Anaconda3\lib\xml\sax\expatreader.py", line 111, in parse
    xmlreader.IncrementalParser.parse(self, source)
  File "C:\ProgramData\Anaconda3\lib\xml\sax\xmlreader.py", line 123, in parse
    buffer = file.read(self._bufsize)
  File "C:\ProgramData\Anaconda3\lib\codecs.py", line 321, in decode
    (result, consumed) = self._buffer_decode(data, self.errors, final)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x92 in position 10: invalid start byte
"""

from __future__ import print_function
from xml.sax import ContentHandler, parse
import requests
import csv
import zipfile
import io

arquivo = requests.get('http://www.al.sp.gov.br/repositorioDados/processo_legislativo/proposituras.zip')
with open('proposituras.zip', 'wb') as compactado:
    compactado.write(arquivo.content)

descompactado = zipfile.ZipFile(io.BytesIO(arquivo.content))
descompactado.extractall()

with open('proposituras.xml','wb') as f:
    f.write(arquivo.content)

class Handler(ContentHandler):

    def __init__(self):
        ContentHandler.__init__(self)
        self.propositura = {}
        self.proposituras = []
        self.current_field = None
        self.in_propositura = False
        self.indent = 0

    def startElement(self, name, attrs):
        print('{}Start element: {}'.format('\t' * self.indent, name))
        self.indent += 1
        if self.in_propositura:
            self.current_field = name
            self.propositura[name] = ''

        if name == 'propositura':
            self.in_propositura = True

    def endElement(self, name):
        self.indent -= 1
        print('{}End element: {}'.format('\t' * self.indent, name))
        if name == 'propositura':
            self.proposituras.append(self.propositura)
            self.propositura = {}
            self.in_propositura = False
            self.current_field = None

    def characters(self, content):
        if content.strip():
            print('{}chars: {}'.format('\t' * self.indent, repr(content)))
        if self.in_propositura and self.current_field:
            self.propositura[self.current_field] += content


def gravar_deputados(writer, proposituras):
    cabecalhos = ['IdDocumento', 'CodOriginalidade', 'Ementa', 
                  'NroLegislativo', 'AnoLegislativo', 'IdNatureza', 
                  'DtEntradaSistema', 'DtPublicacao']
    writer.writerow(cabecalhos)

    for propositura in proposituras:
        writer.writerow([propositura.get(c, '').strip() for c in cabecalhos])


def main():

    handler = Handler()
    with open('proposituras.xml', 'r', encoding='utf-8') as xml_file:
        parse(xml_file, handler)

    print('Encontrados {} proposituras'.format(len(handler.proposituras)))

    with open('proposituras.csv', 'w', encoding='latin-1', newline='') as f_handle:
        writer = csv.writer(f_handle)
        gravar_proposituras(writer, handler.proposituras)


if __name__ == "__main__":
    main()
