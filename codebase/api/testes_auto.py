#Este é um código que deve ser executando usando o pytest. Ele realiza testes automatizados na API em execução.

import requests
import pytest
import time


#Primeiramente, limpar o banco de dados que está persistido...

def teste1():
    response = requests.delete("http://127.0.0.1:5000/api/v1/resetarbd")
    assert response.status_code == 200
    assert response.text == '"Sucesso ao limpar o banco de dados."\n'
    
#Criei uma pauta de 15 minutos.
    
def teste2():
    data = {
        'titulo': 'Pauta criada para testes',
        'tempo': 15
    }
    url = 'http://127.0.0.1:5000/api/v1/cadastrarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert response.text == '"Pauta cadastrada com sucesso!"\n'
    
#Cadastrei um associado.  
    
def teste3():
    data = {
        'nome': 'João Silva',
        'cpf': '677.084.680-27'
    }
    url = 'http://127.0.0.1:5000/api/v1/cadastrarassociado'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert response.text == '"Associado(a) cadastrado(a) com sucesso!"\n'
    
#Tentei votar usando um ID de um associado que não está cadastrado. Deve resultar em erro.


def teste4():
    data = {
'id_associado':'2',
'id_pauta': '1',
'voto':'Sim'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 409
    assert 'existe. Cadastrar em /api/v1/cadastrarassociado"\n' in response.text
    
#Vamos então cadastrá-lo
    
def teste5():
    data = {
        'nome': 'Felipe Abreu',
        'cpf': '495.428.210-18'
    }
    url = 'http://127.0.0.1:5000/api/v1/cadastrarassociado'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert response.text == '"Associado(a) cadastrado(a) com sucesso!"\n'
    
    
#Agora sim será possível votar!    
    
def teste6():
    data = {
'id_associado':'2',
'id_pauta': '1',
'voto':'Sim'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert 'Voto computado com sucesso!' in response.text

    
#O que acontece se o Associado tentar votar de novo? Receberemos então uma mensagem de erro, em status 409.
    
def teste7():
    data = {
'id_associado':'2',
'id_pauta': '1',
'voto':'Sim'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 409
    assert 'votou antes.' in response.text

    
#Criando uma outra pauta, sem declarar a duração. Por padrão, a API vai então aplicar o tempo como 1 minuto.
    
def teste8():
    data = {
        'titulo': 'Mais uma outra pauta criada para testes',
    }
    url = 'http://127.0.0.1:5000/api/v1/cadastrarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert response.text == '"Pauta cadastrada com sucesso!"\n'
    
    
#Retornando todas as pautas

def teste9():

    url = 'http://127.0.0.1:5000/api/v1/retornarpautas'

    response = requests.get(url)

    assert response.status_code == 200
    
    
    
#O que acontece se não utilizarmos "Sim" ou "Não" como voto? A API retornará erro.

    
def teste10():
    data = {
'id_associado':'2',
'id_pauta': '1',
'voto':'a'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 409
    assert 'O voto s\\u00f3 pode ser \\"Sim\\" ou \\"N\\u00e3o\\' in response.text

    
#Vamos então votar com um dos usuários...
    
def teste11():
    data = {
'id_associado':'2',
'id_pauta': '2',
'voto':'Não'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert 'sucesso' in response.text
    #O que vai acontecer se o próximo usuário que tentar votar, vote depois de 1 minuto (tempo que estava definido para esta pauta)
    time.sleep(65)
    
#Será que este outro usuário irá conseguir votar depois de 1 minuto? Ele será recebido com uma mensagem de erro.

def teste12():
    data = {
'id_associado':'1',
'id_pauta': '2',
'voto':'Sim'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 409
    assert 'expirou' in response.text

#Exibir o resultado de uma determinada pauta.
    
def teste11():
    data = {
'id_pauta': '2',
    }
    url = 'http://127.0.0.1:5000/api/v1/resultadopauta'

    response = requests.get(url, json=data)

    assert response.status_code == 200

#Votando na pauta em aberto (de 15 minutos) com o novo usuário:
    
def teste12():
    data = {
'id_associado':'1',
'id_pauta': '1',
'voto':'Sim'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert 'sucesso' in response.text
    
    
#Retornando os votos.
    
def teste13():

    url = 'http://127.0.0.1:5000/api/v1/retornarvotos'

    response = requests.get(url)

    assert response.status_code == 200
    
    
#Retornando os associados cadastrados.
    
    
def teste13():

    url = 'http://127.0.0.1:5000/api/v1/retornarassociados'

    response = requests.get(url)

    assert response.status_code == 200
    
    
#Se um CPF for válido E o Associado estiver cadastrado, deverá retornar como apto para votar
    
def teste14():

    url = 'http://127.0.0.1:5000/api/v1/users/495.428.210-18'

    response = requests.get(url)

    assert response.status_code == 200
    assert 'ABLE_TO_VOTE' in response.text
    
    
#Nesse caso, o CPF está inválido, o que resultará em erro.
    
def teste15():

    url = 'http://127.0.0.1:5000/api/v1/users/1234567890'

    response = requests.get(url)

    assert response.status_code == 404
