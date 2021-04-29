#Importando bibliotecas, declarações e variáveis do arquivo principal. Também usando um alias para a definição "app", pois cria ambiguidade quando se utiliza Flask e pode resultar em erros.

from app import *
import app as aplicacao
from io import StringIO

#Rota para cadastrar pauta, recebendo em JSON o título da pauta e a sua duração em minutos. Por padrão, quando nenhum tempo é declarado, ele define a duração como 1 minuto.

@appflask.route('/api/v1/contentbased', methods=['POST'])
def contentbased():
    jsofile = request.json
    df = aplicacao.pd.read_json(json.dumps(jsofile))
    export_csv = df.to_csv (r'data.csv', index = None, header=True)
    return aplicacao.initrecontent()
     #   return jsonify("Erro ao cadastrar pauta: "+str(e)), 409
    #return jsonify("Pauta cadastrada com sucesso!"), 201



@appflask.route('/api/v1/collaborative', methods=['POST'])
def collaborative():
    jsofile = request.json
    df = aplicacao.pd.read_json(StringIO(json.dumps(jsofile)))
    export_csv = df.to_csv (r'data.csv', index = None, header=True)
    return aplicacao.collab_rec()


    
@appflask.route('/api/v1/resetarbd', methods=["DELETE"])
def resetarbd():
    try:
        aplicacao.resetar_banco(aplicacao.engine)
        return jsonify("Sucesso ao limpar o banco de dados."), 200
    except Exception as e:
        return jsonify("Erro ao tentar limpar o banco de dados: "+str(e)), 405


#HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

#@appflask.route('/api/v1/debug', methods=HTTP_METHODS)
#def debug():
    #aplicacao.localizar_id_por_cpf("057.818.205-07")
    #aplicacao.associadoexiste(2)
    #aplicacao.resetar_banco(aplicacao.engine)
