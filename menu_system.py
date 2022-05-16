import pandas as pd
import pymysql

# product_list = pd.read_csv('products.csv')
empty_product_list = []
while True:
    print("Main Menu\n0. SAVE CHANGES & EXIT\n1. product\n2. courier\n3. order")
    user_input_for_main_menu = input("Please choose what's next: ")
    print("-" * 50)

    if user_input_for_main_menu == "0":
        # SAVE products list to products.csv
        # SAVE couriers list to couriers.csv
        # SAVE orders list to order.csv
        # EXIT app
        if len(empty_product_list) != 0:
            try:
                product_list = pd.read_csv('products.csv')
            except pd.errors.EmptyDataError:
                df1 = pd.DataFrame.from_dict(empty_product_list[0])
                df1.to_csv('products.csv', mode='w')
                try:
                    for a_product in empty_product_list[1:]:
                        df1 = pd.DataFrame.from_dict(a_product)
                        df1.to_csv('products.csv', mode='a', index=False, header=False)
                except ValueError:
                    pass
            else:
                for a_product in empty_product_list:
                    df1 = pd.DataFrame.from_dict(a_product)
                    df1.to_csv('products.csv', mode='a', index=False, header=False)
            print("Product menu has been successfully updated!")
            break
        else:
            print("Nothing has been changed. Exit successfully.")
            break


    while user_input_for_main_menu == "1":
        print("Product Menu\n0. return to main menu\n1. check product menu\n2. add new product to menu\n3. update existing product\n4. delete product")
        user_input_for_product = input("Please choose what's next: ")
        print("-" * 50)
        if user_input_for_product == "0":
            break
        elif user_input_for_product == "1":
            if len(empty_product_list) == 0:
                print("There is nothing in the product list.")
                print("-" * 50)
            else:
                print(empty_product_list)
                print("-" * 50)
        elif user_input_for_product == "2":
            print("You are adding new product to the menu.")
            product = input("product name: ").casefold()
            while True:
                try:
                    price = float(input(f"price for {product}: "))
                    break
                except ValueError:
                    print("Please type in valid price!")
            new_product_and_price = {
                'product': f'{product}',
                'price': f'{price}'
            }
            print(new_product_and_price)
            empty_product_list.append(new_product_and_price)
            print(empty_product_list)
            print("Your change is pending. Please go back to main menu and save it!")
            print("-" * 50)
        elif user_input_for_product == "3":

        else:
            print("!!!Please choose a valid option!!!")
            print("-" * 50)

    if user_input_for_main_menu != "0" and user_input_for_main_menu != "1" and user_input_for_main_menu != "2" and user_input_for_main_menu != "3":
        print("!!!Please choose a valid option!!!")
        print("-" * 50)