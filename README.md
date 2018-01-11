# Caecus

[![Code Health](https://landscape.io/github/rodolfo-viana/caecus/master/landscape.svg?style=flat)](https://landscape.io/github/rodolfo-viana/caecus/master) 

### O que é?
Caecus é (ou pretende ser) uma coleção de scripts relacionados aos deputados estaduais de São Paulo: proposições apresentadas, leis aprovadas, presenças em sessões, andamento de comissões, lista de funcionários, gastos, salários e mais.

### Como funciona?
Os dados apresentados no Caecus são disponibilizados pela Assembleia Legislativa do Estado de São Paulo por meio do [Portal dos Dados Abertos](https://www.al.sp.gov.br/dados-abertos/). Ou seja, a atualização das informações é feita automaticamente, de acordo com a frequência da Alesp.

Também pretendo incluir dados que não estão no portal, por meio de raspagem do site da Alesp.

Os scripts disponíveis rodam com Python 3.

### Quais bibliotecas são necessárias para usar os scripts?
Eu tenho feito testes com algumas bibliotecas, o que significa que a lista muda todos os dias. Já usei lxml, bs4, untangle e outras. Mas, por ora, para os scripts aqui disponíveis, basta instalar pandas e requests.

Para instalar ambas as bibliotecas, no prompt de comando, digite `pip install pandas` e `pip install requests`.

Quando e se a lista de bibliotecas aumentar, crio um arquivo `requirements.txt` aqui.

### Por que Caecus?
"Caecus" significa "cego" em latim. Foi o apelido dado a Ápio Cláudio, político romano que viveu de 340 a.C a 273 a.C. Ele foi responsável por abrir o Senado aos cidadãos dos estratos mais baixos da sociedade, aos comerciantes e aos filhos de ex-escravos. Queria aproximar o povo do poder, e este é o objeto do Caecus. Leia mais sobre Ápio Cláudio na [Wikipédia](https://pt.wikipedia.org/wiki/%C3%81pio_Cl%C3%A1udio_Cego).

### Tem sugestões, correções, dicas?
Você pode abrir uma [issue](https://github.com/rodolfo-viana/caecus/issues), clonar o repositório e mandar um [pull request](https://github.com/rodolfo-viana/caecus/pulls) ou enviar um e-mail para rodolfo arroba rodolfoviana ponto com ponto br.
