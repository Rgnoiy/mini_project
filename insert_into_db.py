import sqlalchemy
import pandas as pd

conn = sqlalchemy.create_engine('mysql+pymysql://root:123456@localhost:3366/mini_project')

sql = '''
select * from courier
where courier_id = 1;
'''

df = pd.read_sql(sql, conn)
print(df)
a = pd.DataFrame.to_dict(df)
print(a)