from pprint import pprint
import sqlalchemy
from sqlalchemy import *
import pandas as pd
from sqlalchemy.dialects.mysql import INTEGER, FLOAT
from sqlalchemy.orm import sessionmaker

conn = create_engine('mysql+pymysql://root:123456@localhost:3366/mini_project')
metadata = MetaData(conn)
DBsession = sessionmaker(bind=conn)
session = DBsession()

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
if __name__ == '__main__':
    _ = pd.DataFrame({"courier_id": [1, 2, 3], "courier_name": ['Mike', 'John', 'Mary'],
                      "courier_phone": ['07264759682', '07294756384', '07593575834']})
    _.to_sql('couriers', con=conn, if_exists='append', index=False)

    _ = pd.DataFrame({"customer_name": ['Oli B', 'Mia Y', 'Henry S'],
                      "customer_address": ["Flat 12, 56A Lant Street, London", '14, Howerd Way, London',
                                           '6, Combwell Crescent, London'],
                      "customer_phone": ['07673172120', '01689446622', '01322276751'],
                      "courier_id": [1, 3, 3],
                      "ordered_items": ['1', '1,2,3', '3']})
    _.to_sql('orders', con=conn, if_exists='append', index=False)

    _ = pd.DataFrame({"product_name": ["Cookie", "Coke", "Latte"],
                      "price": [2.34, 3.59, 1.23]})
    _.to_sql("products", con=conn, if_exists='append', index=False)

    _ = pd.DataFrame({"order_status": ['preparing', 'delivering', 'delivered', 'canceled']})
    _.to_sql("order_status", con=conn, if_exists='append', index=False)


def print_orders_list():
    sql = '''SELECT order_id, customer_name, customer_address, customer_phone, courier_id, ordered_items, order_status 
    FROM orders LEFT OUTER JOIN order_status 
    on orders.order_status_id = order_status.order_status_id'''
    df = pd.read_sql(sql, conn)
    d_series = df.to_dict('records')
    pprint(d_series, sort_dicts=False, width=70)


def print_couriers_list():
    sql = f"""select * from couriers"""
    df = pd.read_sql(sql, conn)
    d_series = df.to_dict('records')
    pprint(d_series, sort_dicts=False, width=70)


def print_order_status_list():
    sql = f"""select * from order_status"""
    df = pd.read_sql(sql, conn)
    d_series = df.to_dict('records')
    pprint(d_series, sort_dicts=False, width=70)


def print_products_list():
    sql = f"""select * from products"""
    df = pd.read_sql(sql, conn)
    d_series = df.to_dict('records')
    pprint(d_series, sort_dicts=False, width=50)


def create_order():
    print("You are creating new order. \nAll fields are required. \nType '0' to return to order menu.")
    sql = '''SELECT * FROM orders'''
    df = pd.read_sql(sql, conn, index_col='customer_phone')
    while True:
        first_name = input("Please enter your first name: ").title().strip().replace(' ', '')
        if first_name == '0':
            print("-" * 80)
            break
        last_name = input("Please enter your last name: ").title().replace(' ', '')
        if last_name == '0':
            print("-" * 80)
            break
        if check_if_empty(first_name, last_name):
            name = first_name + ' ' + last_name
            print('↓\n↓')
            break
        else:
            print("name field cannot be empty.")

    try:
        while name:
            phone = input("Please enter your phone number: ")
            phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+', '')
            if phone == '0':
                print("-" * 80)
                break
            if check_if_empty(phone):
                if phone.isalnum():
                    if phone in df.index:
                        print(f"{phone} already exists. Please try again.")
                    else:
                        print('↓\n↓')
                        break
                else:
                    print("phone format error. Please try again.")
            else:
                print("Phone number cannot be empty.")
    except NameError:
        pass

    try:
        while phone != '0':
            address_1 = input("Please enter your flat/house/building number/name: ").strip()
            if address_1 == '0':
                print("-" * 80)
                break
            address_2 = input("Please enter street name: ").strip().title()
            if address_2 == '0':
                print("-" * 80)
                break
            address_3 = input("Please enter city: ").strip().title()
            if address_3 == '0':
                print("-" * 80)
                break
            address_4 = input("Please enter post-code: ").upper().strip()
            if address_4 == '0':
                print("-" * 80)
                break
            if check_if_empty(address_1, address_2, address_3, address_4):
                address = address_1 + ', ' + address_2 + ', ' + address_3 + ', ' + address_4
                print('↓\n↓')
                break
            else:
                print("All fields are required. Please try again.")
    except NameError:
        pass

    try:
        if address_1 != '0' and address_2 != '0' and address_3 != '0' and address_4 != '0':
            sql = """select * from couriers"""
            print_couriers_list()
            df2 = pd.read_sql(sql, conn, index_col='courier_id')
            while True:
                courier_id = input("Please choose your courier from the list: ").strip()
                if courier_id == '0':
                    print("-" * 80)
                    break
                elif check_if_empty(courier_id):
                    try:
                        input_index = int(courier_id)
                        if input_index in df2.index:
                            print('↓\n↓')
                            break
                        else:
                            print(f"ID {courier_id} is out of range. Please try again.")
                    except ValueError:
                        print(f"Sorry, {courier_id} is not a valid courier code.")
                else:
                    print("Input cannot be empty. Please try again.")
    except NameError:
        pass

    try:
        if courier_id != '0':
            sql = """select * from products"""
            print_products_list()
            df1 = pd.read_sql(sql, conn, index_col='product_id')
            while True:
                ordered_items = input("Please choose id of product "
                                      "you want to order and separate them with ',': ").replace(' ', ',').replace(',,', ',').strip(',')
                data_checking = ordered_items.split(',')
                if ordered_items == '0':
                    print("-" * 80)
                    break
                elif check_if_product_list_input_valid(data_checking, df1):
                    break
                else:
                    pass
    except NameError:
        pass

    try:
        if ordered_items != '0':
            _ = pd.DataFrame({"customer_name": [name],
                              "customer_address": [address],
                              "customer_phone": [phone],
                              "courier_id": [courier_id],
                              "ordered_items": [ordered_items]})
            _ = _.to_sql("orders", con=conn, if_exists='append', index=False)
            while True:
                k = input("Proceed(Y/N)?").casefold()
                if k in ('yes', 'y'):
                    session.commit()
                    print(f"New order has been added.")
                    break
                elif k in ('no', 'n'):
                    print("Your change has not been saved. You will return to order menu.")
                    break
                else:
                    print(f"Invalid choice: {k}")
    except NameError:
        pass


def add_new_product():
    sql = """select * from products"""
    df1 = pd.read_sql(sql, conn, index_col='product_name')
    print("You are adding new product. \nAll fields are required. \nType '0' to return to product menu.")
    while True:
        product_name = input("Please enter product name: ").title().strip()
        if product_name == '0':
            break
        elif check_if_empty(product_name):
            if product_name in df1.index:
                print(f"{product_name} already exists.")
            else:
                break
        else:
            print("name field cannot be empty.")

    try:
        while product_name != '0':
            price = input(f"Please enter the price for {product_name}: ").strip().replace(',', '.')
            if price == '0':
                break
            elif check_if_empty(price):
                try:
                    price = float(price)
                    if price > 0:
                        print(f"Price for {product_name} is £{price}.")
                        break
                    else:
                        print("Price must be positive.")
                except ValueError:
                    print("Input must be number.")
            else:
                print("Price field cannot be empty.")
    except NameError:
        pass

    try:
        if price != '0':
            _ = pd.DataFrame({"product_name": [product_name],
                              "price": [price]})
            _ = _.to_sql("products", con=conn, if_exists='append', index=False)
            while True:
                k = input("Proceed(Y/N)?").casefold()
                if k == 'yes' or k == 'y':
                    session.commit()
                    print("New product has been added.")
                    break
                elif k == 'n' or k == 'no':
                    print("You will return to product menu.")
                    break
                else:
                    print(f"Invalid choice: {k}")
    except NameError:
        pass


def add_new_courier():
    print("You are adding new courier. \nAll fields are required. \nType '0' to return to courier menu.")
    while True:
        first_name = input("Please enter your first name: ").title().strip()
        if first_name == '0':
            break
        last_name = input("Please enter your last name: ").title().strip()
        if last_name == '0':
            break
        elif check_if_empty(first_name, last_name):
            courier_name = first_name + ' ' + last_name
            break
        else:
            print("Name field cannot be empty.")

    try:
        while courier_name:
            courier_phone = input("Please enter your mobile phone number: ")
            courier_phone = courier_phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace(
                '+', '')
            if courier_phone == '0':
                break
            elif check_if_empty(courier_phone):
                if courier_phone.isalnum():
                    break
                else:
                    print("phone format error. Please try again.")
            else:
                print("Phone number cannot be empty.")
    except NameError:
        pass

    try:
        if courier_phone != '0':
            _ = pd.DataFrame({"courier_name": [courier_name],
                              "courier_phone": [courier_phone]})
            _ = _.to_sql("couriers", con=conn, if_exists='append', index=False)
            while True:
                k = input("Proceed(Y/N)?").casefold()
                if k in ('yes', 'y'):
                    session.commit()
                    print("New courier has been added.")
                    break
                elif k in ('no', 'n'):
                    print("You will return to courier menu.")
                    break
                else:
                    print(f"Invalid choice: {k}")
    except NameError:
        pass


def delete_product_list():
    sql = """select * from products"""
    print_products_list()
    df1 = pd.read_sql(sql, conn, index_col='product_id')
    switch = True
    while True:
        if not switch:
            break
        input_index = input("Please choose the id of which you want to delete or type '0' to EXIT: ").replace(' ', '')
        if input_index == '0' or input_index.casefold() == 'exit':
            print("-" * 80)
            print("You've returned to product menu.")
            break
        elif check_if_empty(input_index):
            try:
                input_index = int(input_index)
                if input_index in df1.index:
                    _ = session.query(products).filter_by(product_id=input_index).delete()
                    while True:
                        k = input("Proceed(Y/N)?").casefold()
                        if k in ('yes', 'y'):
                            session.commit()
                            print(f"product {input_index} has been deleted.")
                            break
                        elif k in ('no', 'n'):
                            break
                        else:
                            print(f"Invalid choice: {k}")
                else:
                    print(f"id {input_index} is out of range. Please try again!")
                    continue
            except ValueError:
                print(f"Sorry, {input_index} is not a valid product code!")
                continue
        else:
            print("Input cannot be empty. Please try again.")
            continue
        print('-' * 80)
        print("What do you want to do next?\n1. delete another product\n2. go back to product menu.")
        while True:
            b = input('-->')
            if b == '1':
                switch = True
                print('-' * 80)
                break
            elif b == '2':
                switch = False
                print('-' * 80)
                break
            else:
                print(f'{b} is not valid. Please try again')


def delete_order_list():
    sql = '''SELECT order_id, customer_name, customer_address, customer_phone, courier_id, ordered_items, order_status 
    FROM orders LEFT OUTER JOIN order_status 
    on orders.order_status_id = order_status.order_status_id'''
    print_orders_list()
    df1 = pd.read_sql(sql, conn, index_col='order_id')
    switch = True
    while True:
        if not switch:
            break
        input_index = input("Please choose the id of which you want to delete or type '0' to EXIT: ").replace(' ', '')
        if input_index == '0' or input_index.casefold() == 'exit':
            print("-" * 80)
            print("You've returned to order menu.")
            break
        elif check_if_empty(input_index):
            try:
                input_index = int(input_index)
                if input_index in df1.index:
                    _ = session.query(orders).filter_by(order_id=input_index).delete()
                    while True:
                        k = input("Proceed(Y/N)?").casefold()
                        if k in ('yes', 'y'):
                            session.commit()
                            print(f"order {input_index} has been deleted.")
                            break
                        elif k in ('no', 'n'):
                            break
                        else:
                            print(f"Invalid choice: {k}")
                else:
                    print(f"ID {input_index} is out of range. Please try again.")
                    continue
            except ValueError:
                print(f"Sorry, {input_index} is not a valid order code!")
                continue
        else:
            print("Input cannot be empty. Please try again.")
            continue
        print("-" * 80)
        print("What do you want to do next?\n1. delete another order\n2. go back to order menu.")
        while True:
            b = input('-->')
            if b == '1':
                switch = True
                print('-' * 80)
                break
            elif b == '2':
                switch = False
                print("-" * 80)
                break
            else:
                print(f'{b} is not valid. Please try again')


def delete_courier_list():
    sql = """select * from couriers"""
    print_couriers_list()
    df1 = pd.read_sql(sql, conn, index_col='courier_id')
    switch = True
    while True:
        if not switch:
            break
        input_index = input("Please choose the id of which you want to delete or type '0' to EXIT: ").replace(' ', '')
        if input_index == '0' or input_index.casefold() == 'exit':
            print("-" * 80)
            print("You've returned to courier menu.")
            break
        elif check_if_empty(input_index):
            try:
                input_index = int(input_index)
                if input_index in df1.index:
                    _ = session.query(couriers).filter_by(courier_id=input_index).delete()
                    while True:
                        k = input("Proceed(Y/N)?").casefold()
                        if k in ('yes', 'y'):
                            session.commit()
                            print(f"Courier {input_index} has been deleted.")
                            break
                        elif k in ('no', 'n'):
                            break
                        else:
                            print(f"Invalid choice: {k}")
                else:
                    print(f"ID {input_index} is out of range. Please try again!")
                    continue
            except ValueError:
                print(f"Sorry, {input_index} is not a valid courier code!")
                continue
        else:
            print("Input cannot be empty. Please try again.")
            continue
        print('-' * 80)
        print("What do you want to do next?\n1. delete another courier\n2. go back to courier menu.")
        while True:
            b = input('-->')
            if b == '1':
                switch = True
                print('-' * 80)
                break
            elif b == '2':
                switch = False
                print('-' * 80)
                break
            else:
                print(f'{b} is not valid. Please try again')


def update_existing_product():
    print("You are updating product list. Leave it blank if you don't want to update it. \n"
          "Press '0' to return to product menu.")
    sql = """select * from products"""
    print_products_list()
    df1 = pd.read_sql(sql, conn, index_col='product_id')
    while True:
        input_id = input("Please choose the id of which you want to update: ").replace(' ', '')
        if input_id == '0':
            break
        if check_if_empty(input_id):
            try:
                input_id = int(input_id)
                if input_id in df1.index:
                    break
                else:
                    print(f"Sorry, id {input_id} is out of range. Please try again.")
            except ValueError:
                print(f"{input_id} is not valid for product id.")
        else:
            print("Product id cannot be empty. Please try again.")

    while input_id != '0':
        input_product_name = input(f"Please specify product name for product {input_id} or leave it blank: ").strip().title()
        if input_product_name == '0':
            break
        if check_if_empty(input_product_name):
            try:
                _ = session.query(products).filter_by(product_id=input_id).update({'product_name': input_product_name})
                break
            except sqlalchemy.exc.IntegrityError:
                print(f"{input_product_name} already exists. Please try again.")
        else:
            print(f"Product name of {input_id} will remain the same.")
            break

    try:
        while input_id != '0' and input_product_name != '0':
            input_price = input(f"Please enter the price for product {input_id}: ").strip().replace(',', '.')
            if input_price == '0':
                break
            if check_if_empty(input_price):
                try:
                    input_price = float(input_price)
                    if input_price > 0:
                        session.query(products).filter_by(product_id=input_id).update({'price': input_price})
                        break
                    else:
                        print("Price must be positive.")
                except ValueError:
                    print("Input must be number.")
            else:
                print(f"Price for product {input_id} will remain the same.")
                break
    except NameError:
        pass

    try:
        if input_id != '0' and input_price != '0':
            while True:
                k = input("Proceed(Y/N)?").casefold()
                if k in ('yes', 'y'):
                    session.commit()
                    print(f"Product {input_id} has been updated.")
                    break
                elif k in ('no', 'n'):
                    print("Your change has not been saved.")
                    print("-" * 80)
                    print("You've returned to product menu.")
                    break
                else:
                    print(f"Invalid choice: {k}")
        else:
            print('-' * 80)
            print("You've returned to product menu.")
    except NameError:
        print('-' * 80)
        print("You've returned to product menu.")


def update_existing_courier():
    print("You are updating courier list. Leave it blank if you don't want to update it. \n"
          "Type '0' to return to product menu.")
    sql = """select * from couriers"""
    print_couriers_list()
    df1 = pd.read_sql(sql, conn, index_col='courier_id')
    while True:
        input_id = input("Please choose the id of which you want to update: ").replace(' ', '')
        if input_id == '0':
            break
        if check_if_empty(input_id):
            try:
                input_id = int(input_id)
                if input_id in df1.index:
                    break
                else:
                    print(f"Sorry, id {input_id} is out of range. Please try again.")
            except ValueError:
                print(f"{input_id} is not valid for product id.")
        else:
            print("Courier id cannot be empty. Please try again.")

    while input_id != '0':
        list_of_name = df1.loc[input_id, "courier_name"].split(' ')
        first_name = input(f"Please specify the first name for courier {input_id}: ").title().replace(' ', '')
        if first_name == '0':
            break
        if check_if_empty(first_name):
            pass
        else:
            first_name = list_of_name[0]
            print(f"First name for courier {input_id} will remain the same.")
        last_name = input(f"Please enter new last name for order {input_id}: ").title().replace(' ', '')
        if last_name == '0':
            break
        if check_if_empty(last_name):
            pass
        else:
            last_name = list_of_name[1]
            print(f"Last name for courier {input_id} will remain the same.")
        input_courier_name = first_name + ' ' + last_name
        _ = session.query(couriers).filter_by(courier_id=input_id).update({"courier_name": input_courier_name})
        break

    try:
        while input_courier_name != '0':
            input_phone = input(f"Please enter the phone for courier {input_id}: ")
            input_phone = input_phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+', '')
            if input_phone == '0':
                break
            if check_if_empty(input_phone):
                if input_phone.isalnum():
                    try:
                        _ = session.query(couriers).filter_by(courier_id=input_id).update({'courier_phone': input_phone})
                        break
                    except sqlalchemy.exc.IntegrityError:
                        print(f"{input_phone} already exists. Please try again.")
                else:
                    print("phone format error. Please try again.")
            else:
                print(f"Phone number for courier {input_id} will remain the same.")
                break
    except NameError:
        pass

    try:
        if input_phone != '0':
            while True:
                k = input("Proceed(Y/N)?").casefold()
                if k in ('yes', 'y'):
                    session.commit()
                    print(f"Courier {input_id} has been updated.")
                    print("-" * 80)
                    break
                elif k in ('no', 'n'):
                    print("Your change has not been saved.")
                    print("-" * 80)
                    print("You've returned to courier menu.")
                    break
                else:
                    print(f"Invalid choice: {k}")
        else:
            print("Your change has not been saved.")
            print('-' * 80)
            print("You've returned to courier menu.")
    except NameError:
        print('-' * 80)
        print("You've returned to courier menu.")


def update_status_in_order_table():
    print("You are updating order status. Leave if black if you\nType '0' to return to order menu.")
    sql = '''SELECT order_id, customer_name, customer_address, customer_phone, courier_id, ordered_items, order_status 
    FROM orders LEFT OUTER JOIN order_status 
    on orders.order_status_id = order_status.order_status_id'''
    df1 = pd.read_sql(sql, conn, index_col='order_id')
    sql2 = '''SELECT * FROM order_status'''
    df2 = pd.read_sql(sql2, conn, index_col='order_status_id')
    print_orders_list()
    print()
    print_order_status_list()
    while True:
        input_id = input("Please choose the order you want to update by selecting id: ").replace(' ', '')
        if input_id == '0':
            break
        if check_if_empty(input_id):
            try:
                input_id = int(input_id)
                if input_id in df1.index:
                    break
                else:
                    print(f"Sorry, id {input_id} is out of range. Please try again.")
            except ValueError:
                print(f"{input_id} is not valid for order id.")
        else:
            print("Order id cannot be empty. Please try again.")

    while input_id != '0':
        input_status_id = input("Please choose the id of status:").replace(' ', '')
        if input_status_id == '0':
            break
        if check_if_empty(input_status_id):
            try:
                input_status_id = int(input_status_id)
                if input_status_id in df2.index:
                    _ = session.query(orders).filter_by(order_id=input_id).update({'order_status_id': input_status_id})
                    break
                else:
                    print(f"Sorry, id {input_status_id} is out of range. Please try again.")
            except ValueError:
                print(f"{input_id} is not valid for order id.")
        else:
            print("Status id cannot be empty. Please try again.")

    try:
        if input_status_id != '0':
            while True:
                k = input("Proceed(Y/N)?").casefold()
                if k in ('yes', 'y'):
                    session.commit()
                    print(f"Status for order {input_id} has been updated.")
                    break
                elif k in ('no', 'n'):
                    print("Your change has not been saved.")
                    print("-" * 80)
                    print("You've returned to order menu.")
                    break
                else:
                    print(f"Invalid choice: {k}")
        else:
            print('-' * 80)
            print("You've returned to order menu.")
    except NameError:
        print('-' * 80)
        print("You've returned to order menu.")


def update_order():
    sql = '''SELECT order_id, customer_name, customer_address, customer_phone, courier_id, ordered_items, order_status 
    FROM orders LEFT OUTER JOIN order_status 
    on orders.order_status_id = order_status.order_status_id'''
    df1 = pd.read_sql(sql, conn, index_col='order_id')
    while True:
        print_orders_list()
        print("You are updating order. Leave it blank if you don't want to update it.\nAlways type '0' to EXIT.")
        input_id = input("Please choose the order you want to update by selecting order id: ").replace(' ', '')
        if input_id == '0':
            print("-" * 80)
            break
        if check_if_empty(input_id):
            try:
                input_id = int(input_id)
                if input_id in df1.index:
                    pass
                else:
                    print(f"Sorry, id {input_id} is out of range. Please try again.")
                    print("-" * 80)
                    continue
            except ValueError:
                print(f"{input_id} is not valid for order id.")
                print("-" * 80)
                continue
        else:
            print("Order id cannot be empty. Please try again.")
            print("-" * 80)
            continue

        while input_id != '0':
            print("-" * 80)
            print(f"Please choose which you want to update for ORDER {input_id} next:"
                  "\nSub Menu"
                  "\n1. customer name"
                  "\n2. customer address"
                  "\n3. customer phone number"
                  "\n4. ordered items"
                  "\n5. courier id"
                  "\n0. return to order selection")
            choice = input()
            try:
                if int(choice) in range(6):
                    switch = True
                else:
                    print(f"{choice} is not valid. Please try again.")
                    continue
            except ValueError:
                print(f"{choice} is not valid. Please try again.")
                continue

            if choice == '0':
                break

            while choice == '1':
                if not switch:
                    break
                list_of_name = df1.loc[input_id, 'customer_name'].split(' ')
                first_name = input(f"Please enter new first name for order {input_id}: ").title().replace(' ', '')
                if first_name == '0':
                    break
                if check_if_empty(first_name):
                    pass
                else:
                    first_name = list_of_name[0]
                    print(f"First name for order {input_id} will remain the same.")
                last_name = input(f"Please enter new last name for order {input_id}: ").title().replace(' ', '')
                if last_name == '0':
                    break
                if check_if_empty(last_name):
                    pass
                else:
                    last_name = list_of_name[1]
                    print(f"Last name for order {input_id} will remain the same.")
                input_customer_name = first_name + ' ' + last_name
                _ = session.query(orders).filter_by(order_id=input_id).update({"customer_name": input_customer_name})
                while True:
                    k = input("Proceed(Y/N)?").casefold()
                    if k in ('yes', 'y'):
                        session.commit()
                        print(f"Name for {input_id} has been updated.")
                        break
                    elif k in ('no', 'n'):
                        break
                    else:
                        print(f"Invalid choice: {k}")
                print("What do you want to do next?\n1. Re-enter name\n2. go back to sub menu.")
                while True:
                    b = input('-->')
                    if b == '1':
                        switch = True
                        print("-" * 80)
                        break
                    elif b == '2':
                        switch = False
                        break
                    else:
                        print(f'{b} is not valid. Please try again')

            while choice == '3':
                if not switch:
                    break
                input_phone = input(f"Please enter a new phone number for order {input_id}: ")
                input_phone = input_phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+', '')
                if input_phone == '0':
                    break
                if check_if_empty(input_phone):
                    if input_phone.isalnum():
                        try:
                            _ = session.query(orders).filter_by(order_id=input_id).update({'customer_phone': input_phone})
                            while True:
                                k = input("Proceed(Y/N)?").casefold()
                                if k in ('yes', 'y'):
                                    session.commit()
                                    print(f"Phone number for order {input_id} has been updated.")
                                    break
                                elif k in ('no', 'n'):
                                    break
                                else:
                                    print(f"Invalid choice: {k}")
                        except sqlalchemy.exc.IntegrityError:
                            print(f"{input_phone} already exists. Please try again.")
                            continue
                    else:
                        print("phone format error. Please try again.")
                        continue
                else:
                    print(f"Phone number for order {input_id} will remain the same.")
                print("-" * 80)
                print("What do you want to do next?\n1. Re-enter phone number\n2. go back to sub menu")
                while True:
                    b = input('-->')
                    if b == '1':
                        switch = True
                        print("-" * 80)
                        break
                    elif b == '2':
                        switch = False
                        break
                    else:
                        print(f'{b} is not valid. Please try again')

            while choice == '2':
                if not switch:
                    break
                list_of_address = df1.loc[input_id, 'customer_address'].split(', ')
                address_1 = input("Please enter your flat/house/building number/name: ")
                address_1 = address_1.strip().title().replace(', ', ' ').replace(',', ' ')
                if address_1 == '0':
                    break
                if check_if_empty(address_1):
                    pass
                else:
                    address_1 = list_of_address[0]
                    print(f"Flat/house/building number/name will remain the same for order {input_id}.")
                address_2 = input("Please enter street name: ")
                address_2 = address_2.strip().title().replace(', ', ' ').replace(',', ' ')
                if address_2 == '0':
                    break
                if check_if_empty(address_2):
                    pass
                else:
                    address_2 = list_of_address[1]
                    print(f"Street name will remain the same for order {input_id}.")
                address_3 = input("Please enter city: ")
                address_3 = address_2.strip().title().replace(', ', ' ').replace(',', ' ')
                if address_3 == '0':
                    break
                if check_if_empty(address_3):
                    pass
                else:
                    address_3 = list_of_address[2]
                    print(f"City will remain the same for order {input_id}.")
                address_4 = input("Please enter post-code: ").upper()
                if address_4 == '0':
                    break
                if check_if_empty(address_4):
                    pass
                else:
                    address_4 = list_of_address[3]
                    print(f"Post code will remain the same for order {input_id}.")
                if check_if_empty(address_1, address_2, address_3, address_4):
                    address = address_1 + ', ' + address_2 + ', ' + address_3 + ', ' + address_4
                    _ = session.query(orders).filter_by(order_id=input_id).update({'customer_address': address})
                    while True:
                        k = input("Proceed(Y/N)?").casefold()
                        if k in ('yes', 'y'):
                            session.commit()
                            print(f"Address for order {input_id} has been updated.")
                            break
                        elif k in ('no', 'n'):
                            break
                        else:
                            print(f"Invalid choice: {k}")
                    print("What do you want to do next?\n1. Re-enter address\n2. go back to sub menu")
                    while True:
                        b = input('-->')
                        if b == '1':
                            switch = True
                            print("-" * 80)
                            break
                        elif b == '2':
                            switch = False
                            break
                        else:
                            print(f'{b} is not valid. Please try again')

            if choice == '5':
                print("-" * 80)
                sql = """select * from couriers"""
                print_couriers_list()
                df2 = pd.read_sql(sql, conn, index_col='courier_id')
                while True:
                    if not switch:
                        break
                    courier_id = input("Please change your courier: ").strip()
                    if courier_id == '0':
                        break
                    elif check_if_empty(courier_id):
                        try:
                            input_index = int(courier_id)
                            if input_index in df2.index:
                                _ = session.query(orders).filter_by(order_id=input_id).update({'courier_id': courier_id})
                                while True:
                                    k = input("Proceed(Y/N)?").casefold()
                                    if k in ('yes', 'y'):
                                        session.commit()
                                        print(f"Courier for order {input_id} has been updated.")
                                        break
                                    elif k in ('no', 'n'):
                                        break
                                    else:
                                        print(f"Invalid choice: {k}")
                            else:
                                print(f"ID {courier_id} is out of range. Please try again.")
                                continue
                        except ValueError:
                            print(f"Sorry, {courier_id} is not a valid courier code!")
                            continue
                    else:
                        print(f"Courier for order {input_id} will remain the same.")
                    print("-" * 80)
                    print("What do you want to do next?\n1. Re-enter courier id\n2. go back to sub menu")
                    while True:
                        b = input('-->')
                        if b == '1':
                            switch = True
                            print("-" * 80)
                            break
                        elif b == '2':
                            switch = False
                            break
                        else:
                            print(f'{b} is not valid. Please try again')

            if choice == '4':
                sql = """select * from products"""
                print_products_list()
                df3 = pd.read_sql(sql, conn, index_col='product_id')
                while True:
                    if not switch:
                        break
                    ordered_items = input("Please choose id of product "
                                          "you want to update and separate them with ',': ").replace(' ', '').replace(',,', ',').strip(',')
                    data_checking = ordered_items.split(',')
                    if ordered_items == '0':
                        break
                    if not check_if_empty(ordered_items):
                        print(f"Ordered items for order {input_id} will remain the same.")
                    elif check_if_product_list_input_valid(data_checking, df3):
                        _ = session.query(orders).filter_by(order_id=input_id).update({'ordered_items': ordered_items})
                        while True:
                            k = input("Proceed(Y/N)?").casefold()
                            if k in ('yes', 'y'):
                                session.commit()
                                print(f"Ordered items for order {input_id} has been updated.")
                                break
                            elif k in ('no', 'n'):
                                break
                            else:
                                print(f"Invalid choice: {k}")
                    else:
                        continue
                    print("-" * 80)
                    print("What do you want to do next?\n1. Re-enter ordered items\n2. go back to sub menu")
                    while True:
                        b = input('-->')
                        if b == '1':
                            switch = True
                            print("-" * 80)
                            break
                        elif b == '2':
                            switch = False
                            break
                        else:
                            print(f'{b} is not valid. Please try again.')


def check_if_empty(*a: str):
    for b in a:
        if b.isspace() or len(b) == 0:
            return False
    return True


def check_if_product_list_input_valid(a: list, df):
    for b in a:
        if check_if_empty(b):
            try:
                input_index = int(b)
                if input_index in df.index:
                    pass
                else:
                    print(f"ID {b} is out of range. Please try again.")
                    return False
            except ValueError:
                print(f"Sorry, {b} is not a valid product code.")
                return False
        else:
            print("Input cannot be empty. Please try again.")
            return False
    return True


# add_new_courier('Sam', '9376328928')
# add_new_product('ice-coffee', 3.45)
# add_new_product('coke', 4.34)
# add_new_product('cookie', 3.5)
# add_new_status("")
# delete_order_list()
# sql = '''SELECT order_id, customer_name, customer_address, customer_phone, courier_id, ordered_items, order_status
#     FROM orders LEFT OUTER JOIN order_status
#     on orders.order_status_id = order_status.order_status_id'''
# df1 = pd.read_sql(sql, conn, index_col='order_id')
# a = df1.loc[5, 'customer_name'].split(' ')
# print(a)
# update_order()
session.close()