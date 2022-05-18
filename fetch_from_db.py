import pymysql
from sqlalchemy import *
import pandas as pd
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER, FLOAT

conn = create_engine('mysql+pymysql://root:123456@localhost:3366/mini_project')
metadata = MetaData(conn)
# conn_pysql = pymysql.connect(user='root', password='123456', host='localhost', database='mini_project', port=3366,
#                              charset='utf8')
# mycursor = conn_pysql.cursor()

if __name__ == '__main__':
    couriers = Table('couriers', metadata,
                     Column('courier_id', Integer, nullable=False, primary_key=True, autoincrement=True),
                     Column('courier_name', VARCHAR(45), nullable=False),
                     Column('courier_phone', CHAR(20), nullable=False, unique=True))
    orders = Table('orders', metadata,
                   Column('order_id', Integer, nullable=False, primary_key=True, autoincrement=True),
                   Column('customer_name', VARCHAR(45), nullable=False),
                   Column('customer_address', VARCHAR(60), nullable=False),
                   Column('customer_phone', VARCHAR(45), nullable=False, unique=True),
                   Column('courier_id', INTEGER, nullable=False),
                   Column('order_status', VARCHAR(20), nullable=False, server_default='unknown'))
    products = Table('products', metadata,
                     Column('product_id', Integer, primary_key=True, nullable=False, autoincrement=True),
                     Column('product_name', VARCHAR(50), unique=True, nullable=False),
                     Column('price', FLOAT(unsigned=True), nullable=False))
    ordered_items = Table('ordered_items', metadata,
                          Column('order_id', Integer, nullable=False),
                          Column('ordered_items', Integer, nullable=False))
    metadata.create_all()

    _ = pd.DataFrame({"courier_id": [1, 2, 3], "courier_name": ['Mike', 'John', 'Mary'],
                      "courier_phone": ['07264759682', '07294756384', '07593575834']})
    _.to_sql('couriers', con=conn, if_exists='append', index=False)

    _ = pd.DataFrame({"order_id": [1, 2, 3],
                      "customer_name": ['Oli', 'Bala', 'Saira'],
                      "customer_address": ['Flat 12, 56A Lant Street, London', '14 Howerd Way, London',
                                           '6 Combwell Crescent, London'],
                      "customer_phone": ['(020) 7317 2120', '(01689) 446622', '(01322) 276751'],
                      "courier_id": [1, 3, 3],
                      "order_status": ['preparing', 'preparing', 'preparing']})
    _.to_sql('orders', con=conn, if_exists='append', index=False)

    _ = pd.DataFrame({"order_id": [1, 1, 1, 2, 2, 3],
                      "ordered_items": [4, 3, 5, 6, 7, 8]})
    _.to_sql("ordered_items", con=conn, if_exists='append', index=False)


sql = '''
select ordered_items from mini_project.ordered_items
left join mini_project.orders
on ordered_items.order_id = orders.order_id
'''
# # def print_order_list
#     """select * from order
#        outer join ordered_items
#        on ordered_items.order_id = order.order_id"""
# # def print_courier_list
#     """select * from courier"""
# # def print_product_list
#     """select * from mini_project.product"""
# def ordered_items():
#     """select ordered_items from mini_project.ordered_items
#        left join mini_project.order
#        on ordered_items.order_id = order.order_id"""

df = pd.read_sql(sql, conn)
print(df)
a = pd.DataFrame.to_dict(df)        # fix the index
print(a)
