import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sqlalchemy import *
import time


def itemDesc(id,ds):
    return ds.loc[ds['itemId'] == id]['description'].tolist()[0]

def itemName(id,ds):
    return ds.loc[ds['itemId'] == id]['title'].tolist()[0]

# Just reads the results out of the dictionary.
def recommend(ds,results,item_id, num):
    end = "Recommending " + str(num) + " items similar to " + itemName(item_id,ds) + "..."
    end = end + "<br>" + "-------"
    recs = results[item_id][:num]
    for rec in recs:
        end = end + "<br>" + "Recommended: " +"Name:  "+itemName(rec[1],ds)+ ";"+ itemDesc(rec[1],ds) + " (score:" + str(rec[0]) + ")"
    return end


def start(dbn,itid):
    start = time.perf_counter()
    dataprocessstart = time.perf_counter()
    print('sqlite:///./db'+str(dbn)+'.db?check_same_thread=False')
    engine = create_engine('sqlite:///./db'+str(dbn)+'.db?check_same_thread=False')

    ds = pd.read_sql_query('''SELECT * FROM items''', con=engine)
    dataprocessend = time.perf_counter() - dataprocessstart
    recstart = time.perf_counter()

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['description']+"|"+ds['tag'])

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    results = {}

    for idx, row in ds.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], ds['itemId'][i]) for i in similar_indices]

        results[row['itemId']] = similar_items[1:]

    print('done!')
    string = recommend(ds,results,item_id=itid, num=10)
    recend = time.perf_counter() - recstart
    end = time.perf_counter() - start
    return "Total API endpoint execution time: "+str(end)+"<br>"+"Data processing time: "+str(dataprocessend)+"<br>"+"Recommendation execution time: "+str(recend)+"<br>"+string
