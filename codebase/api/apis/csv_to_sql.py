import pandas
import sqlalchemy

engine = create_engine('sqlite:///cdb.db')
Base.metadata.create_all(engine)

file_name = 'client_db.csv'
df = pandas.read_csv(file_name)
df.to_sql(con=engine, index_label='id', name=cdb1.__tablename__, if_exists='replace')