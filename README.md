# Caecus

[![Documentation Status](http://readthedocs.org/projects/caecus/badge/?version=latest)](http://caecus.readthedocs.io/en/latest/?badge=latest) [![Code Health](https://landscape.io/github/rodolfo-viana/caecus/master/landscape.svg?style=flat)](https://landscape.io/github/rodolfo-viana/caecus/master) [![Test Coverage](https://api.codeclimate.com/v1/badges/9763052d5a3c6f5c86dd/test_coverage)](https://codeclimate.com/github/rodolfo-viana/caecus/test_coverage) [![Maintainability](https://api.codeclimate.com/v1/badges/9763052d5a3c6f5c86dd/maintainability)](https://codeclimate.com/github/rodolfo-viana/caecus/maintainability) [![](https://img.shields.io/badge/made%20with-%3C3-red.svg)](https://rodolfoviana.com.br/)

### O que é
Caecus é (ou pretende ser) uma coleção de scripts para download de dados relacionados aos deputados estaduais de São Paulo: proposições apresentadas, leis aprovadas, presenças em sessões, andamento de comissões, lista de funcionários, gastos, salários e mais.

### Quais são os scripts
Há três scripts prontos: 

* `scraper_alesp_deputados.py` (informações sobre os deputados atuais, como nomes, partidos, telefones, biografias, situação etc.; v.1.1), 
* `scraper_alesp_funcionarios.py` (informações sobre os funcionários da Alesp, como nomes, lotações, quando começaram e quando saíram dos cargos; v.1.0), e 
* `scraper_alesp_gastos_gabinetes.py` (dados sobre despesas dos deputados reembolsadas pela verba de gabinete, como valores, fornecedores, CNPJ/CPF, categorias de despesas etc.). 

Outros scripts estão em desenvolvimento, e estarão à disposição depois de alguns testes.

### De onde vêm os dados
Os dados apresentados no Caecus são disponibilizados pela Assembleia Legislativa do Estado de São Paulo por meio do [Portal dos Dados Abertos](https://www.al.sp.gov.br/dados-abertos/). Ou seja, a atualização das informações é feita automaticamente, de acordo com a frequência da Alesp. 

Também pretendo incluir dados que não estão no portal, por meio de raspagem do site da Alesp.

### Como uso os scripts
Você precisa ter Python 3 no seu computador. O download pode ser feito pelo [site oficial](https://www.python.org/downloads/) ou por uma distribuição, como [Anaconda](https://www.anaconda.com/download/) -- é a que eu uso e recomendo, pois já vem com a maioria das bibliotecas necessárias. 

Caso opte pelo Python 3 "puro", você terá de baixar as bibliotecas uma a uma. Recomendo que siga as instruções [desse vídeo](https://www.youtube.com/watch?v=AnIDjAilIzM) para instalar `pip` e `virtualenv` -- o vídeo traz a versão 2.7 do Python, mas o passo a passo é o mesmo para o Python 3.

Depois da instalação, crie uma pasta de trabalho. No prompt de comando, digite:
```
$ mkdir nomedapastadetrabalho
$ cd nomedapastadetrabalho
```

Agora é hora de criar um ambiente de trabalho. Se instalou o Python "puro", digite:
```
$ virtualenv nomedoambientequevocequiser
$ activate nomedoambientequevocequiser
$ pip install pandas
$ pip install requests
```

Se baixou Anaconda, digite:
```
$ conda create --name nomedoambientequevocequiser python=3
$ activate nomedoambientequevocequiser
```

Com o ambiente criado, digite:
```
$ git clone https://github.com/rodolfo-viana/caecus/
$ cd caecus
```

Pronto! Os arquivos estão copiados no seu computador. Para usar um dos scripts, digite:
```
$ python nomedoscript.py
```

Não se esqueça: sempre que quiser usar um dos scripts, é preciso entrar na pasta `caecus`, digitar `activate nomedoambientequevocequiser` e, só então, digitar `python nomedoscript.py`.

### Quais bibliotecas são necessárias para usar os scripts
Eu tenho feito testes com algumas bibliotecas, o que significa que a lista muda todos os dias. Já usei lxml, bs4, untangle e outras. Mas, por ora, para os scripts aqui disponíveis, basta instalar pandas e requests, conforme descrito acima. Quando e se a lista de bibliotecas aumentar, crio um arquivo `requirements.txt` aqui.

### Por que Caecus
"Caecus" significa "cego" em latim. Foi o apelido dado a Ápio Cláudio, político romano que viveu de 340 a.C a 273 a.C. Ele foi responsável por abrir o Senado aos cidadãos dos estratos mais baixos da sociedade, aos comerciantes e aos filhos de ex-escravos. Queria aproximar o povo do poder, e este é o objeto do Caecus. 

Leia mais sobre Ápio Cláudio na [Wikipédia](https://pt.wikipedia.org/wiki/%C3%81pio_Cl%C3%A1udio_Cego).

### Tem sugestões ou correções, ou quer colaborar de alguma forma?
Você pode abrir uma [issue](https://github.com/rodolfo-viana/caecus/issues), clonar o repositório e mandar um [pull request](https://github.com/rodolfo-viana/caecus/pulls) ou enviar um e-mail para rodolfo arroba rodolfoviana ponto com ponto br.
