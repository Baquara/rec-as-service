import pandas as pd



df =  pd.read_csv('entrada.csv', sep=','  , engine='python')


print(f"Dataframe:\n{df}\n")
for row, col in df.iterrows():
    #print(f"Row Index:{row}")
    assert col.count() == df.shape[1]
    print(f"Column:\n{col}\n")
    for x in col:
        assert isinstance(x,int)