import pymysql
from sqlalchemy import *
import pandas as pd
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER, FLOAT

conn = create_engine('mysql+pymysql://root:123456@localhost:3366/mini_project')
metadata = MetaData(conn)

if __name__ == '__main__':
    couriers = Table('couriers', metadata,
                     Column('courier_id', INTEGER, nullable=False, primary_key=True, autoincrement=True),
                     Column('courier_name', VARCHAR(50), nullable=False),
                     Column('courier_phone', CHAR(20), nullable=False, unique=True))
    orders = Table('orders', metadata,
                   Column('order_id', Integer, nullable=False, primary_key=True, autoincrement=True),
                   Column('customer_name', VARCHAR(45), nullable=False),
                   Column('customer_address', VARCHAR(60), nullable=False),
                   Column('customer_phone', VARCHAR(45), nullable=False, unique=True),
                   Column('courier_id', INTEGER, nullable=False),
                   Column('order_status', INTEGER, nullable=False, server_default='1'),
                   Column('ordered_items', VARCHAR(50), nullable=False))
    products = Table('products', metadata,
                     Column('product_id', Integer, primary_key=True, nullable=False, autoincrement=True),
                     Column('product_name', VARCHAR(50), unique=True, nullable=False),
                     Column('price', FLOAT(unsigned=True), nullable=False)
                     )
    metadata.create_all()
# if __name__ == '__main__':
#     _ = pd.DataFrame({"courier_id": [1, 2, 3], "courier_name": ['Mike', 'John', 'Mary'],
#                       "courier_phone": ['07264759682', '07294756384', '07593575834']})
#     _.to_sql('couriers', con=conn, if_exists='append', index=False)
#
#     _ = pd.DataFrame({"order_id": [1, 2, 3],
#                       "customer_name": ['Oli', 'Bala', 'Saira'],
#                       "customer_address": ['Flat 12, 56A Lant Street, London', '14 Howerd Way, London',
#                                            '6 Combwell Crescent, London'],
#                       "customer_phone": ['(020) 7317 2120', '(01689) 446622', '(01322) 276751'],
#                       "courier_id": [1, 3, 3],
#                       "ordered_items": ["1", "1, 2, 3", "3"]})
#     _.to_sql('orders', con=conn, if_exists='append', index=False)
#     _ = pd.DataFrame({"product_id": [1, 2, 3],
#                       "product_name": ["cookie", "coke", "latte"],
#                       "price": [2.34, 3.59, 1.23]})
#     _.to_sql("products", con=conn, if_exists='append', index=False)


sql = '''
select * from orders
'''


# def print_orders_list():
#     sql = '''select * from orders'''
#     df = pd.read_sql(sql, conn)
#     d_series = df.to_dict('records')
#     print(d_series)
#
#
# def print_couriers_list():
#     sql = """select * from couriers"""
#     df = pd.read_sql(sql, conn)
#     d_series = df.to_dict('records')
#     print(d_series)
#
#
# def print_products_list():
#     sql = """select * from products"""
#     df = pd.read_sql(sql, conn)
#     d_series = df.to_dict('records')
#     print(d_series)

# def create_order(name:str, address:str, phone:str, product:str, )

# def delete_order():

df = pd.read_sql(sql, conn)
print(df)
d_series = df.to_dict('records')
print(d_series)

# for a in d_series:
#     print(a)
