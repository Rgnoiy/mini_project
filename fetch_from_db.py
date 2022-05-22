from pprint import pprint, pformat

import numpy as np
from sqlalchemy import *
import pandas as pd
from sqlalchemy.dialects.mysql import INTEGER, FLOAT
from sqlalchemy.orm import sessionmaker

conn = create_engine('mysql+pymysql://root:123456@localhost:3366/mini_project')
metadata = MetaData(conn)
DBsession = sessionmaker(bind=conn)
session = DBsession()
if __name__ == '__main__':
    couriers = Table('couriers', metadata,
                     Column('courier_id', INTEGER, nullable=False, primary_key=True, autoincrement=True),
                     Column('courier_name', VARCHAR(50), nullable=False),
                     Column('courier_phone', CHAR(20), nullable=False, unique=True))
    orders = Table('orders', metadata,
                   Column('order_id', Integer, nullable=False, primary_key=True, autoincrement=True),
                   Column('customer_name', VARCHAR(45), nullable=False),
                   Column('customer_address', VARCHAR(60), nullable=False),
                   Column('customer_phone', VARCHAR(45), nullable=False),
                   Column('courier_id', INTEGER, nullable=False),
                   Column('order_status_id', INTEGER, nullable=False, server_default='1'),
                   Column('ordered_items', VARCHAR(50), nullable=False))
    products = Table('products', metadata,
                     Column('product_id', Integer, primary_key=True, nullable=False, autoincrement=True),
                     Column('product_name', VARCHAR(50), unique=True, nullable=False),
                     Column('price', FLOAT(unsigned=True), nullable=False)
                     )
    order_status = Table('order_status', metadata,
                         Column('order_status_id', INTEGER, primary_key=True, nullable=False, autoincrement=True),
                         Column('order_status', VARCHAR(50), nullable=False, unique=True))
    metadata.create_all()
    # _ = pd.DataFrame({"courier_id": [1, 2, 3], "courier_name": ['Mike', 'John', 'Mary'],
    #                   "courier_phone": ['07264759682', '07294756384', '07593575834']})
    # _.to_sql('couriers', con=conn, if_exists='append', index=False)

    # _ = pd.DataFrame({"customer_name": ['Oli', 'Bala', 'Saira'],
    #                   "customer_address": ["Flat 12, 56A Lant Street, London", '14 Howerd Way, London',
    #                                        '6 Combwell Crescent, London'],
    #                   "customer_phone": ['07673172120', '01689446622', '01322276751'],
    #                   "courier_id": [1, 3, 3],
    #                   "ordered_items": ['1', '1,2,3', '3']})
    # _.to_sql('orders', con=conn, if_exists='append', index=False)

    # _ = pd.DataFrame({
    #                   "product_name": ["cookie", "coke", "latte"],
    #                   "price": [2.34, 3.59, 1.23]})
    # _.to_sql("products", con=conn, if_exists='append', index=False)

    # _ = pd.DataFrame({"order_status": ['preparing', 'delivering', 'delivered', 'canceled']})
    # _.to_sql("order_status", con=conn, if_exists='append', index=False)


def print_orders_list():
    sql = '''SELECT order_id, customer_name, customer_address, customer_phone, courier_id, ordered_items, order_status 
    FROM orders LEFT OUTER JOIN order_status 
    on orders.order_status_id = order_status.order_status_id'''
    df = pd.read_sql(sql, conn)
    d_series = df.to_dict('records')
    pprint(d_series, sort_dicts=False)


def print_list(table_name):
    sql = f"""select * from {table_name}"""
    df = pd.read_sql(sql, conn)
    d_series = df.to_dict('records')
    pprint(d_series, sort_dicts=False)


def create_order():
    print("You are creating new order. \nAll fields are required. \nType 'E' to return to order menu.")
    while True:
        first_name = input("Please enter your first name: ").title().strip()
        if first_name.casefold() == 'e':
            break
        last_name = input("Please enter your last name: ").title().strip()
        if last_name.casefold() == 'e':
            break
        elif check_if_empty(first_name) and check_if_empty(last_name):
            name = first_name + ' ' + last_name
            break
        else:
            print("name field cannot be empty.")

    try:
        while name:
            phone = input("Please enter your mobile phone number: ")
            phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+', '')
            if phone.casefold() == 'e':
                break
            elif check_if_empty(phone):
                if phone.isalnum():  # ?
                    break
                else:
                    print("phone format error. Please try again.")
            else:
                print("Phone number cannot be empty.")
    except NameError:
        pass

    while phone.casefold() != 'e':
        address_1 = input("Please enter your flat/house/building number/name: ").strip()
        if address_1.casefold() == 'e':
            break
        address_2 = input("Please enter street: ").strip()
        if address_2.casefold() == 'e':
            break
        address_3 = input("Please enter city: ").strip()
        if address_3.casefold() == 'e':
            break
        address_4 = input("Please enter post-code: ").upper().strip()
        if address_4.casefold() == 'e':
            break
        elif check_if_empty(address_1, address_2, address_3, address_4):
            address = address_1 + ', ' + address_2 + ', ' + address_3 + ', ' + address_4
            break
        else:
            print("All fields are required. Please try again.")
    while address:


        print_list(products)
        ordered_items = input("Please choose id of product you want to order and separate them with ','")
    _ = pd.DataFrame({"customer_name": [name],
                      "customer_address": [address],
                      "customer_phone": [phone],
                      "courier_id": [courier_id],
                      "ordered_items": [ordered_items]})
    _ = _.to_sql("orders", con=conn, if_exists='append', index=False)
    print("Your order has been created.")


def add_new_product(product_name: str, price: float):
    _ = pd.DataFrame({"product_name": [product_name],
                      "price": [price]})
    _ = _.to_sql("products", con=conn, if_exists='append', index=False)
    print("Product has been added.")


def add_new_courier(courier_name: str, courier_phone: str):
    _ = pd.DataFrame({"courier_name": [courier_name],
                      "courier_phone": [courier_phone]})
    _ = _.to_sql("couriers", con=conn, if_exists='append', index=False)
    print("Courier has been added.")


# def add_new_status(order_status):
#     _ = pd.DataFrame({"order_status": [order_status]})
#     _ = _.to_sql("order_status", con=conn, if_exists='append', index=False)
#     print("Status has been added.")


def delete_product_list():
    sql = """select * from products"""
    print_list(products)
    df1 = pd.read_sql(sql, conn, index_col='product_id')
    while True:
        input_index = input("Please choose the id of which you want to delete or type 'E' to EXIT: ")
        if input_index.casefold() == 'e' or input_index.casefold() == 'exit':
            break
        elif check_if_empty(input_index):
            try:
                input_index = int(input_index)
                if input_index in df1.index:
                    _ = session.query(products).filter_by(product_id=input_index).delete()
                    while True:
                        k = input("Proceed(Y/N)?").casefold()
                        if k == 'yes' or k == 'y':
                            session.commit()
                            print(f"product {input_index} has been deleted.")
                            break
                        elif k == 'n' or k == 'no':
                            break
                        else:
                            print(f"Invalid choice: {k}")
                else:
                    print(f"id {input_index} is out of range. Please try again!")
            except ValueError:
                print(f"Sorry, {input_index} is not a valid courier code!")
        else:
            print("Input cannot be empty. Please try again.")
    # session.close()


def delete_order_list():
    sql = '''SELECT order_id, customer_name, customer_address, customer_phone, courier_id, ordered_items, order_status 
    FROM orders LEFT OUTER JOIN order_status 
    on orders.order_status_id = order_status.order_status_id'''
    print_orders_list()
    df1 = pd.read_sql(sql, conn, index_col='order_id')
    while True:
        input_index = input("Please choose the id of which you want to delete or type 'E' to EXIT: ")
        if input_index.casefold() == 'e' or input_index.casefold() == 'exit':
            break
        elif check_if_empty(input_index):
            try:
                input_index = int(input_index)
                if input_index in df1.index:
                    _ = session.query(orders).filter_by(order_id=input_index).delete()
                    while True:
                        k = input("Proceed(Y/N)?").casefold()
                        if k == 'yes' or k == 'y':
                            session.commit()
                            print(f"order {input_index} has been deleted.")
                            break
                        elif k == 'n' or k == 'no':
                            break
                        else:
                            print(f"Invalid choice: {k}")
                else:
                    print(f"ID {input_index} is out of range. Please try again!")
            except ValueError:
                print(f"Sorry, {input_index} is not a valid order code!")
        else:
            print("Input cannot be empty. Please try again.")


def delete_courier_list():
    sql = """select * from couriers"""
    print_list(couriers)
    df1 = pd.read_sql(sql, conn, index_col='courier_id')
    while True:
        input_index = input("Please choose the id of which you want to delete or type 'E' to EXIT: ")
        if input_index.casefold() == 'e' or input_index.casefold() == 'exit':
            break
        elif check_if_empty(input_index):
            try:
                input_index = int(input_index)
                if input_index in df1.index:
                    _ = session.query(couriers).filter_by(courier_id=input_index).delete()
                    while True:
                        k = input("Proceed(Y/N)?").casefold()
                        if k == 'yes' or k == 'y':
                            session.commit()
                            print(f"Courier {input_index} has been deleted.")
                            break
                        elif k == 'n' or k == 'no':
                            break
                        else:
                            print(f"Invalid choice: {k}")
                else:
                    print(f"ID {input_index} is out of range. Please try again!")
            except ValueError:
                print(f"Sorry, {input_index} is not a valid courier code!")
        else:
            print("Input cannot be empty. Please try again.")


# def update_order_status():


def check_if_empty(*a: str):
    for b in a:
        if b.isspace() or len(b) == 0:
            return False
        else:
            return True


# def check_if_int(a: str):
#     try:
#         int(a)
#         return True
#     except ValueError:
#         return False


def update_existing_product(input_id: int):
    print("Please type in new value. Leave it blank if you don't want to update the same.")
    input_value = input("product name: ")
    session.query(products).filter_by(id=input_id).update({products.product_name: input_value})

# add_new_courier('Sam', '9376328928')
# add_new_product('ice-coffee', 3.45)
# add_new_product('coke', 4.34)
# add_new_product('cookie', 3.5)
# add_new_status("")
# delete_order_list()
while True:
    first_name = input("Please enter your first name: ").title().strip()
    if first_name.casefold() == 'e':
        break
    last_name = input("Please enter your last name: ").title().strip()
    if last_name.casefold() == 'e':
        break
    elif check_if_empty(first_name) and check_if_empty(last_name):
        name = first_name + ' ' + last_name
        break
    else:
        print("name field cannot be empty.")

try:
    while name:
        phone = input("Please enter your mobile phone number: ")
        phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+', '')
        if phone.casefold() == 'e':
            break
        elif check_if_empty(phone):
            if phone.isalnum():  # ?
                break
            else:
                print("phone format error. Please try again.")
        else:
            print("Phone number cannot be empty.")
except NameError:
    pass

try:
    while phone.casefold() != 'e':
        address_1 = input("Please enter your flat/house/building number/name: ").strip()
        if address_1.casefold() == 'e':
            break
        address_2 = input("Please enter street name: ").strip().title()
        if address_2.casefold() == 'e':
            break
        address_3 = input("Please enter city: ").strip().title()
        if address_3.casefold() == 'e':
            break
        address_4 = input("Please enter post-code: ").upper().strip()
        if address_4.casefold() == 'e':
            break
        elif check_if_empty(address_1, address_2, address_3, address_4):
            address = address_1 + ', ' + address_2 + ', ' + address_3 + ', ' + address_4
            break
        else:
            print("All fields are required. Please try again.")
except NameError:
    pass

try:
    if address:
        sql = """select * from couriers"""
        print_list(couriers)
        df1 = pd.read_sql(sql, conn, index_col='courier_id')
        while True:
            courier_id = input("Please choose your courier: ").strip()
            if courier_id.casefold() == 'e':
                break
            elif check_if_empty(courier_id):
                try:
                    input_index = int(courier_id)
                    if input_index in df1.index:
                        break
                    else:
                        print(f"ID {courier_id} is out of range. Please try again!")
                except ValueError:
                    print(f"Sorry, {courier_id} is not a valid courier code!")
            else:
                print("Input cannot be empty. Please try again.")
except NameError:
    pass

try:
    if courier_id:
        sql = """select * from products"""
        print_list(products)
        df1 = pd.read_sql(sql, conn, index_col='product_id')
        while True:
            ordered_items = input("Please choose id of product you want to order and separate them with ',': ").replace(', ', ',')
            data_checking = ordered_items.split(',')
            if ordered_items == 'e':
                break
            else:
                for a in data_checking:
                    b = a.strip()
                    if check_if_empty(b):
                        try:
                            input_index = int(b)
                            if input_index in df1.index:
                                print(f'{b} passed')
                            else:
                                print(f"ID {b} is out of range. Please try again!")
                        except ValueError:
                            print(f"Sorry, {b} is not a valid product code!")
                    else:
                        print("Input cannot be empty. Please try again.")
except NameError:
    pass
# _ = pd.DataFrame({"customer_name": [name],
#                   "customer_address": [address],
#                   "customer_phone": [phone],
#                   "courier_id": [courier_id],
#                   "ordered_items": [ordered_items]})
# _ = _.to_sql("orders", con=conn, if_exists='append', index=False)
# while True:
#     k = input("Proceed(Y/N)?").casefold()
#     if k == 'yes' or k == 'y':
#         session.commit()
#         print(f"Courier {input_index} has been deleted.")
#         break
#     elif k == 'n' or k == 'no':
#         break
#     else:
#         print(f"Invalid choice: {k}")
# print("Your order has been created.")