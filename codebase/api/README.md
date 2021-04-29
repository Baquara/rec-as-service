# Desafio-backend-python

Repositório com a solução de um desafio para vaga de Backend.

Esta solução foi elaborada no Framework Flask, na Linguagem Python. Para fins de portabilidade, o banco de dados utilizado para este projeto (cujo pré-requisito é persistência de dados) é SQLite.

As rotas de API se encontram inteiramente documentadas na seguinte URL do Postman:

https://documenter.getpostman.com/view/13068940/Tz5jefpE


Também criei uma branch para uma versão dockerizada do projeto (em caráter experimental), porém recomendo realizar a configuração do environment de acordo com a branch principal.


## Arquitetura do Projeto

Este projeto possui um código principal (app.py) onde as principais bibliotecas utilizadas são importadas bem como as funções auxiliares, um arquivo com o core do projeto contendo todas as rotas de API (api.py), e um arquivo com o banco de dados persistente (banco.py).

Portanto, para o estudo da API em si, o principal arquivo é api.py.

Este projeto também conta com testes automatizados. Para executar os testes automatizados, no diretório principal e com a aplicação em execução, utilizar:

>pytest testes_auto.py

Conforme sinalizado no texto do desafio, para este projeto não foi incluído segurança nas rotas utilizando JWT, sendo assim as rotas estão em livre acesso para debugging.

## Dependências

É necessário ter o Python 3 instalado no sistema. Quando o repositório do projeto for clonado, deve-se executar:

>pip install -r requirements.txt

## Como executar

Clonar o projeto:

>git clone https://github.com/Baquara/Desafio-backend-python.git

Em seguida,

>cd Desafio-backend-python
>
>pip install -r requirements.txt
>
>export FLASK_APP=app.py
>
>flask run

Por padrão a aplicação é executada em http://127.0.0.1:5000/ .

Em seguida, verificar a documentação das rotas:

https://documenter.getpostman.com/view/13068940/Tz5jefpE


## Testes automatizados:

No diretório principal , está presente o arquivo testes_auto.py, que pode ser executado usando a biblioteca pytest. A API precisa estar em execução na máquina local (http://127.0.0.1:5000/) para que os testes sejam executados. 

>pytest testes_auto.py



