import pandas as pd
import pymysql


empty_product_list = []
while True:
    print("Main Menu\n0. EXIT\n1. product\n2. courier\n3. order")
    user_input_for_main_menu = input("Please choose what's next: ")
    print("-" * 50)

    if user_input_for_main_menu == "0":
            print("Exit successfully.")
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
        elif user_input_for_product == "2":     # FOR NEW PRODUCT
            print("You are adding new product to the menu.")
            product = input("product name: ").casefold()
            while True:
                try:
                    price = float(input(f"price for {product}: "))
                    break
                except ValueError:
                    print("Please type a valid price!")
            # TODO: insert inputs into db
            new_product_and_price = {
                'product': f'{product}',
                'price': f'{price}'
            }
            # print(new_product_and_price)
            # empty_product_list.append(new_product_and_price)
            # print(empty_product_list)
            # print("Your change is pending. Please go back to main menu and save it!")
            print("-" * 50)
        elif user_input_for_product == "3":         # update
            # TODO: 1. get all products from products table and print ALL product IDS
            # TODO: 2. get user input for product ID/name/price
            # TODO: 3. if any inputs are empty, do not update them, do what then..?
            # TODO: 4. UPDATE properties for Products in product table
        elif user_input_for_product == "4":     # DELETE product
            # TODO: 1. get all products and print IDS from products table(duplicate->use def)
            # TODO: 2. get user input for product ID
            # TODO: 3. DELETE product in products table
        else:
            print("!!!Please choose a valid option!!!")
            print("-" * 50)

    while user_input_for_main_menu == "2":
        print("Courier Menu\n0. return to main menu\n1. check couriers list\n2. add new courier to list\n3. update existing courier\n4. delete courier")
        user_input_for_courier = input("Please choose what's next: ")

        if user_input_for_courier == "0":
            break
        elif user_input_for_courier == "1":
            # TODO: print courier list
        elif user_input_for_courier == "2":     # create new courier
            # TODO: get user input for courier name/courier phone number
            # TODO: INSERT courier into couriers table
        elif user_input_for_courier == "3":     # update existing courier
            # TODO: get all couriers from couriers table and print couriers with their IDs
            # TODO: get user input for courier ID/name/phone number
            # TODO: if input is empty, do not update its respective table property
            # TODO: UPDATE properties for courier in courier table
        elif user_input_for_courier == "4":        # DELETE existing courier
            # TODO: get all couriers from couriers table and print couriers with their IDs(duplicate)
            # TODO: get user input for courier ID
            # TODO: delete it from table
        else:
            print("!!!Please choose a valid option!!!")
            print("-" * 50)

    while user_input_for_main_menu == "3":
        print("Order Menu\n0. return to main menu\n1. check order list\n2. add new order to list\n3. update existing product\n4. delete product")
        user_input_for_order = input("Please choose what's next: ")
        if user_input_for_order == "0":
            break
        elif user_input_for_order == "1":
            # TODO: print order dict
        elif user_input_for_order == "2":
            # TODO: user input for name/address(sepreate lines)/phone number
            # TODO: print products list with its index values
            # TODO: get user input for comma-separated list of product index values
                # TODO: convert user input to list of integers
            # TODO: PRINT couriers list with index value for each courier
            # TODO: get user input for courier index to select courier
            # TODO: SET order status to be 'PREPARING'(trigger)
            # TODO: CREATE AND display order as dict with the information provided above
            # TODO: append order to orders list
        elif user_input_for_order == "3":       # update status
            # TODO: PRINT orders list with order_id
            # TODO: GET user input for order_id
            # TODO: PRINT order status list with index values?
            # TODO: Get user input for order status index value?
            # TODO: UPDATE status for order
        elif user_input_for_order == "4":       # update existing order
            # TODO: print orders list with order_id(duplicate)
            # TODO: FOR EACH key-value pair in selected order:
                        #GET user input for updated property
                        #IF user input is blank:
                            #do not update this property
                        #ELSE:
                            #update the property value with user input
        elif user_input_for_order == "5":
            # TODO: print orders list
            # TODO: get user input for order_id
            # TODO: DELETE that order
        else:
            print("!!!Please choose a valid option!!!")
            print("-" * 50)
            

    if user_input_for_main_menu != "0" and user_input_for_main_menu != "1" and user_input_for_main_menu != "2" and user_input_for_main_menu != "3":
        print("!!!Please choose a valid option!!!")
        print("-" * 50)