#Este é o código onde o projeto deverá ser executado. Ele não contém as rotas de API principais, que estão no arquivo api.py, porém contém as funções auxiliares que a API utiliza.


#Estas são as dependências base que eu insiro em meus projetos de API utilizando framework Flask (Python).

from flask import Flask, render_template, request, jsonify, abort
import re
import json
import requests
from sqlalchemy import *
from flask_cors import CORS
import datetime
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel




appflask = Flask(__name__)


#Chama o código com as rotas de API, core do projeto.

import api
import pandas as pd


#Chave que pode ser usada para criptografar banco de dados ou utilizar session.

appflask.secret_key = b'_8#azL"oyt4z\n\xec]/'


#Declaração principal para o banco de dados. Estou usando a biblioteca SQLAlchemy, que é um ORM, é agnóstico em relação a quais tipos de banco de dados é possível utilizar.
#Eu poderia ter utilizado qualquer outro tipo de banco de dados, mas optei pelo SQLite para fins de portabilidade.

engine = create_engine('sqlite:///banco.db')
engine.echo = False



#Função auxiliar para limpar dados do banco de dados. A rota de API "resetarbd" utiliza essa função.

def resetar_banco(session):
    meta = MetaData()
    meta.reflect(bind=session)
    for table in reversed(meta.sorted_tables):
        print ('Limpando tabela  %s' % table)
        session.execute(table.delete())

#Função auxiliar para converter objetos do SQLAlchemy (tabelas/queries do banco) em um JSON manipulável.
        
def convertesql(sqlobj):
    d, a = {}, []
    for rowproxy in sqlobj:
        for column, value in rowproxy.items():
            d = {**d, **{column: value}}
        a.append(d)
    if(a == []):
        return None
    return a
    

def item(id,ds):
    return ds.loc[ds['id'] == id]['description'].tolist()[0].split(' - ')[0]

# Just reads the results out of the dictionary.
def recommend(item_id, num,ds,results):
    print("Recommending " + str(num) + " content similar to " + item(item_id,ds) + "...")
    print("-------")
    recs = results[item_id][:num]
    finalist=[]
    for rec in recs:
        print("Recommended: " + item(rec[1],ds) + " (score:" + str(rec[0]) + ")")
        finalist.append({"Recommended":item(rec[1],ds),"Score":str(rec[0])})
    return jsonify(finalist)


def collab_rec():
    metadata = pd.read_csv('data.csv', low_memory=False)
    metadata.head(3) 
    # Calculate mean of vote average column
    C = metadata['vote_average'].mean()
    print(C)
    # Calculate the minimum number of votes required to be in the chart, m
    m = metadata['vote_count'].quantile(0.90)
    print(m)

    contentlist = metadata.copy().loc[metadata['vote_count'] >= m]
    contentlist.shape

    # Function that computes the weighted rating of each content
    def weighted_rating(x, m=m, C=C):
        v = x['vote_count']
        R = x['vote_average']
        # Calculation
        return (v/(v+m) * R) + (m/(m+v) * C)

    # Define a new feature 'score' and calculate its value with `weighted_rating()`
    contentlist['score'] = contentlist.apply(weighted_rating, axis=1)

    #Sort content based on score calculated above
    contentlist = contentlist.sort_values('score', ascending=False)

    #Print the top 20 from the content
    dataf = contentlist[['title', 'vote_count', 'vote_average', 'score']].head(20)
    result = dataf.to_json(orient="index")
    return(json.loads(result))



def initrecontent():
    ds = pd.read_csv("data.csv")
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['description'])
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    results = {}
    for idx, row in ds.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]
        results[row['id']] = similar_items[1:]
    print('done!')
    return recommend(item_id=11, num=5,ds=ds,results=results)


#Executa a aplicação


if __name__ == "__main__":
    appflask.run()
 
