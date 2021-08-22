#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd



# In[2]:


# read data
df_items = pd.read_sql_table('items', 'postgres:///db_name',

    usecols=['itemId', 'title'],
    dtype={'itemId': 'int32', 'title': 'str'})

df_ratings = pd.read_sql_table('ratings', 'postgres:///db_name',
    usecols=['userId', 'itemId', 'rating'],
    dtype={'userId': 'int32', 'itemId': 'int32', 'rating': 'float32'})


# In[3]:


df_items.head()
df_items.shape


# In[4]:


df_ratings.head()


# In[5]:


# df_ratings.shape
df_ratings=df_ratings[:2000000]


# In[6]:


df_ratings.shape


# In[7]:


from scipy.sparse import csr_matrix
# pivot ratings into item features
df_item_features = df_ratings.pivot(
    index='itemId',
    columns='userId',
    values='rating'
).fillna(0)


# In[8]:


mat_item_features = csr_matrix(df_item_features.values)


# In[9]:


df_item_features.head()


# In[10]:


from sklearn.neighbors import NearestNeighbors
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)


# In[11]:


num_users = len(df_ratings.userId.unique())
num_items = len(df_ratings.itemId.unique())
print('There are {} unique users and {} unique items in this data set'.format(num_users, num_items))


# In[12]:


# get count
df_ratings_cnt_tmp = pd.DataFrame(df_ratings.groupby('rating').size(), columns=['count'])
df_ratings_cnt_tmp


# In[13]:


# there are a lot more counts in rating of zero
total_cnt = num_users * num_items
rating_zero_cnt = total_cnt - df_ratings.shape[0]

df_ratings_cnt = df_ratings_cnt_tmp.append(
    pd.DataFrame({'count': rating_zero_cnt}, index=[0.0]),
    verify_integrity=True,
).sort_index()
df_ratings_cnt


# In[14]:


#log normalise to make it easier to interpret on a graph
import numpy as np
df_ratings_cnt['log_count'] = np.log(df_ratings_cnt['count'])
df_ratings_cnt


# In[15]:


import matplotlib.pyplot as plt
plt.style.use('ggplot')

get_ipython().run_line_magic('matplotlib', 'inline')
ax = df_ratings_cnt[['count']].reset_index().rename(columns={'index': 'rating score'}).plot(
    x='rating score',
    y='count',
    kind='bar',
    figsize=(12, 8),
    title='Count for Each Rating Score (in Log Scale)',
    logy=True,
    fontsize=12,
)
ax.set_xlabel("item rating score")
ax.set_ylabel("number of ratings")


# In[16]:


# get rating frequency
#number of ratings each item got.
df_items_cnt = pd.DataFrame(df_ratings.groupby('itemId').size(), columns=['count'])
df_items_cnt.head()


# In[17]:


#now we need to take only items that have been rated atleast 50 times to get some idea of the reactions of users towards it

popularity_thres = 50
popular_items = list(set(df_items_cnt.query('count >= @popularity_thres').index))
df_ratings_drop_items = df_ratings[df_ratings.itemId.isin(popular_items)]
print('shape of original ratings data: ', df_ratings.shape)
print('shape of ratings data after dropping unpopular items: ', df_ratings_drop_items.shape)


# In[18]:


# get number of ratings given by every user
df_users_cnt = pd.DataFrame(df_ratings_drop_items.groupby('userId').size(), columns=['count'])
df_users_cnt.head()


# In[19]:


# filter data to come to an approximation of user likings.
ratings_thres = 50
active_users = list(set(df_users_cnt.query('count >= @ratings_thres').index))
df_ratings_drop_users = df_ratings_drop_items[df_ratings_drop_items.userId.isin(active_users)]
print('shape of original ratings data: ', df_ratings.shape)
print('shape of ratings data after dropping both unpopular items and inactive users: ', df_ratings_drop_users.shape)


# In[20]:


# pivot and create item-user matrix
item_user_mat = df_ratings_drop_users.pivot(index='itemId', columns='userId', values='rating').fillna(0)
#map item titles to images
item_to_idx = {
    item: i for i, item in 
    enumerate(list(df_items.set_index('itemId').loc[item_user_mat.index].title))
}
# transform matrix to scipy sparse matrix
item_user_mat_sparse = csr_matrix(item_user_mat.values)


# In[21]:


item_user_mat_sparse


# In[22]:


# define model
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
# fit
model_knn.fit(item_user_mat_sparse)


# In[23]:


from fuzzywuzzy import fuzz


# In[24]:


def fuzzy_matching(mapper, fav_item, verbose=True):
    """
    return the closest match via fuzzy ratio. 
    
    Parameters
    ----------    
    mapper: dict, map item title name to index of the item in data
    fav_item: str, name of user input item
    
    verbose: bool, print log if True
    Return
    ------
    index of the closest match
    """
    match_tuple = []
    # get match
    for title, idx in mapper.items():
        ratio = fuzz.ratio(title.lower(), fav_item.lower())
        if ratio >= 60:
            match_tuple.append((title, idx, ratio))
    # sort
    match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
    if not match_tuple:
        print('Oops! No match is found')
        return
    if verbose:
        print('Found possible matches in our database: {0}\n'.format([x[0] for x in match_tuple]))
    return match_tuple[0][1]


# In[25]:


def make_recommendation(model_knn, data, mapper, fav_item, n_recommendations):
    """
    return top n similar item recommendations based on user's input item
    Parameters
    ----------
    model_knn: sklearn model, knn model
    data: item-user matrix
    mapper: dict, map item title name to index of the item in data
    fav_item: str, name of user input item
    n_recommendations: int, top n recommendations
    Return
    ------
    list of top n similar item recommendations
    """
    # fit
    model_knn.fit(data)
    # get input item index
    print('You have input item:', fav_item)
    idx = fuzzy_matching(mapper, fav_item, verbose=True)
    
    print('Recommendation system start to make inference')
    print('......\n')
    distances, indices = model_knn.kneighbors(data[idx], n_neighbors=n_recommendations+1)
    
    raw_recommends =         sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
    # get reverse mapper
    reverse_mapper = {v: k for k, v in mapper.items()}
    # print recommendations
    print('Recommendations for {}:'.format(fav_item))
    for i, (idx, dist) in enumerate(raw_recommends):
        print('{0}: {1}, with distance of {2}'.format(i+1, reverse_mapper[idx], dist))


# In[26]:


my_favorite = 'Iron Man'

make_recommendation(
    model_knn=model_knn,
    data=item_user_mat_sparse,
    fav_item=my_favorite,
    mapper=item_to_idx,
    n_recommendations=10)


# In[27]:


item_to_idx


# In[ ]:
