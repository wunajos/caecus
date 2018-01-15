#!/usr/bin/python3
#-*- coding: utf-8 -*-
###############################################################################
# Crawler de deputados na Assembleia Legislativa do Estado de São Paulo
# Author: rodolfoviana
# License:  MIT License
#
# Copyright (c) 2018 Rodolfo Viana
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################
# Input:
#   [optional:] -x XML input file with propositions (default: proposituras.xml)
#   [optional:] -o CSV file with agreggated data (default: proposituras.csv)
#   [optional:] -l logfile (default: <empty> - no logfile)
# Output:
#   [optional:] -i XML output file with propositions (default: proposituras.xml)
###############################################################################
###############################################################################
# Changelog:
# v0.X (14/01/2018) - Initial version
###############################################################################

"""
Crawler de deputados na Assembleia Legislativa do Estado de São Paulo
Criado em 14 de janeiro de 2018, às 17:27:43
@author: rodolfoviana

--------------------------
| WIP - WORK IN PROGRESS |
--------------------------
"""
from __future__ import print_function
from xml.sax import ContentHandler, parse
import requests
import csv
import zipfile
import io
import argparse
import logging


__AUTHOR__ = "rodolfoviana"
__version__ = "x.x"
__copyright__ = "Copyright 2018 - Rodolfo Viana"
__credits__ = ["Rodolfo Viana"]
__maintainer__ = "Rodolfo Viana"
__email__ = "@rodolfoviana(github)"
__status__ = "build 1"
__BUILD__ = "2018-01-14"
__LICENSE__ = "MIT"


def get_zip(fileIn, logger):
    logger.debug("[GZ00] Iniciando : %s", fileIn)
    url = 'http://www.al.sp.gov.br/repositorioDados/' +\
                                        'processo_legislativo/proposituras.zip'
    logger.debug("[GZ10] Url a puxar : %s", url)
    arquivoUrl = requests.get(url)
    logger.debug("[GZ20] Salvando conteudo do arquivo.")
    with open('proposituras.zip', 'wb') as compactado:
        compactado.write(arquivoUrl.content)
    logger.debug("[GZ30] Arquivo salvo. descompactando.")
    descompactado = zipfile.ZipFile(io.BytesIO(arquivoUrl.content))
    xml = descompactado.extractall()
    logger.debug("[GZ40] Descompactado, salvando.")
    with open(fileIn,'w') as f:
        f.write(xml)
    logger.debug("[GZ50] Arquivo salvo: %s", fileIn)
    
    
class Handler(ContentHandler):

    def __init__(self):
        ContentHandler.__init__(self)
        self.propositura = {}
        self.proposituras = []
        self.current_field = None
        self.in_propositura = False
        self.indent = 0
        self.logger = None
    
    def setLogger(self, logger):
        self.logger = logger

    def startElement(self, name, attrs):
        # print('{}Start element: {}'.format('\t' * self.indent, name))
        self.logger.debug('[H10] {}Start element: {}'.format('\t' * self.indent, 
                                                                    name))
        self.indent += 1
        if self.in_propositura:
            self.current_field = name
            self.propositura[name] = ''

        if name == 'propositura':
            self.in_propositura = True

    def endElement(self, name):
        self.indent -= 1
        # print('{}End element: {}'.format('\t' * self.indent, name))
        self.logger.debug('[H20] {}End element: {}'.format('\t' * self.indent,
                                                                         name))
        if name == 'propositura':
            self.proposituras.append(self.propositura)
            self.propositura = {}
            self.in_propositura = False
            self.current_field = None

    def characters(self, content):
        if content.strip():
            # print('{}chars: {}'.format('\t' * self.indent, repr(content)))
            self.logger.debug('[H30] {}chars: {}'.format('\t' * self.indent, 
                                                                repr(content)))
        if self.in_propositura and self.current_field:
            self.propositura[self.current_field] += content


def setLog(level, fileLog):
    # ##Loglevels:
    # CRITICAL - 50
    # ERROR - 40
    # WARNING - 30
    # INFO - 20 
    # DEBUG - 10 ---> too much log! be aware
    # NOTSET - 0
    fmt = '%(asctime)-20s:%(name)s:%(levelname)-8s= %(message)s' 
    df = '%d/%m/%Y %H:%M:%S'
    if (int(level) == 10) :
        # print('Debug level: 10 (debug)')
        logging.basicConfig(filename=fileLog, format=fmt, datefmt=df, 
                                                        level=logging.DEBUG)
    elif (int(level) == 20):
        # print('Debug level: 20 (info)')
        logging.basicConfig(filename=fileLog, format=fmt, datefmt=df,  
                                                        level=logging.INFO)
    elif (int(level) == 30):
        # print('Debug level: 30 (warning)')
        logging.basicConfig(filename=fileLog, format=fmt, datefmt=df,  
                                                        level=logging.WARNING)
    elif (int(level) == 40):
        # print('Debug level: 40 (error)')
        logging.basicConfig(filename=fileLog, format=fmt, datefmt=df,  
                                                        level=logging.ERROR)
    elif (int(level) == 50):
        # print('Debug level: 50 (critical)')
        logging.basicConfig(filename=fileLog, format=fmt, datefmt=df,  
                                                        level=logging.CRITICAL)
    else:
        # print('Debug level: 0 (not set)')
        logging.basicConfig(filename=fileLog, format=fmt, datefmt=df,  
                                                        level=logging.NOTSET)
    return logging.getLogger(__name__)
    
    
def setArgParser():
    parser = argparse.ArgumentParser(description= 'alespscraprop' + __version__)
    # 0: no log, 50: critical, 40: error, 30: warning*, 20: info, 10: debug
    parser.add_argument('-d', '--debug', nargs='?', dest='debug',
                     default='30', help='Enable more logging')
    parser.add_argument('-i', '--infile', nargs='?', dest='fileIn',
                         default='proposituras.xml', 
                         help='Propositions output new file (xml).')
    parser.add_argument('-x', '--xmlfile', nargs='?', dest='fileXml',
                         default='', 
                      help='Propositions input xml file (already downloaded).')
    parser.add_argument('-l', '--log', nargs='?', dest='fileLog',
                                          default='', help='export debug log.')
    parser.add_argument('-o', '--outfile', nargs='?', dest='fileOut',
                        default='proposituras.csv', 
                        help='Save results in file (csv)')
    parser.add_argument('--version', action='version', version='%(prog)s ' +
                                                             str(__version__))
    return parser.parse_args()

def gravar_props(writer, proposituras, logger):
    logger.info("[GD00] Gravando dados")
    cabecalhos = ['IdDocumento', 'CodOriginalidade', 'Ementa', 
                  'NroLegislativo', 'AnoLegislativo', 'IdNatureza', 
                  'DtEntradaSistema', 'DtPublicacao']
    logger.debug("[GD10] Cabeçalhos: %s", cabecalhos)
    writer.writerow(cabecalhos)
    for propositura in proposituras:
        logger.debug("[GD20]: Propositura %s", propositura)
        writer.writerow([propositura.get(c, '').strip() for c in cabecalhos])


def main():
    args = setArgParser()
    if (args.fileLog == ''):
        logger = setLog(60, args.fileLog)  # sem log
    else:
        logger = setLog(args.debug, args.fileLog)
        logger.debug('[M00]= = = = =  Alesp Proposições Scrapper = = = = = = ')
        
    if (args.fileXml == ''):
        logger.debug('[M05] Sem arquivo XML (puxando do site da alesp). ')
        get_zip(args.fileIn, logger)
        args.fileXml = args.fileIn
    else:
        logger.debug('[M06] Com arquivo XML (já puxado) ')

    logger.debug("[M10] Iniciando com o arquivo: %s", args.fileXml)

    logger.debug("[M20] Chamando o Handler")
    handler = Handler()
    handler.setLogger(logger)
    with open(args.fileXml, 'r', encoding='utf-8') as xml_file:
        logger.debug('[M30] Iniciando a leitura de: %s', xml_file)
        parse(xml_file, handler)

    print('Encontrados {} proposituras'.format(len(handler.proposituras)))
    # não entendi pq nao salvar em utf-8 tbm.
    with open(args.fileOut, 'w', encoding='latin-1', newline='') as f_handle:
        writer = csv.writer(f_handle)
        logger.debug("[M40] Gravando o arquivo: %s", args.fileOut)
        gravar_props(writer, handler.proposituras, logger)
    logger.debug("[M50] Saindo..")
    return 0

if __name__ == "__main__":
    main()
