import fetch_from_db


while True:
    print("Main Menu\n0. EXIT\n1. product\n2. courier\n3. order")
    user_input_for_main_menu = input("Please choose what's next: ")
    print("-" * 80)

    if user_input_for_main_menu == "0":
        print("Exit successfully.")
        break
    while user_input_for_main_menu == "1":
        print("Product Menu\n0. return to main menu\n1. check products list\n"
              "2. add new products to list\n3. update existing product\n4. delete product")
        user_input_for_product = input("Please choose the id of what's next: ")
        print("-" * 80)
        if user_input_for_product == '0':
            break
        elif user_input_for_product == '1':
            fetch_from_db.print_products_list()
            print("-" * 80)
        elif user_input_for_product == "2":     # FOR NEW PRODUCT
            fetch_from_db.add_new_product()
        elif user_input_for_product == "3":         # update
            fetch_from_db.update_existing_product()
        elif user_input_for_product == "4":     # DELETE product
            fetch_from_db.delete_product_list()
        else:
            print(f"{user_input_for_product} is not valid. Please try again.")
            print("-" * 80)

    while user_input_for_main_menu == "2":
        print("Courier Menu\n0. return to main menu\n1. check couriers list\n"
              "2. add new courier to list\n3. update existing courier\n4. delete courier")
        user_input_for_courier = input("Please choose the id of what's next: ")
        print("-" * 80)
        if user_input_for_courier == "0":
            break
        elif user_input_for_courier == "1":
            fetch_from_db.print_couriers_list()
            print("-" * 80)
        elif user_input_for_courier == "2":
            fetch_from_db.add_new_courier()
        elif user_input_for_courier == "3":
            fetch_from_db.update_existing_courier()
        elif user_input_for_courier == "4":
            fetch_from_db.delete_courier_list()
        else:
            print(f"{user_input_for_courier} is not valid. Please try again.")
            print("-" * 80)

    while user_input_for_main_menu == "3":
        print("Order Menu\n0. return to main menu\n1. check order list\n"
              "2. add new order to list\n3. update order status for existing order"
              "\n4. update existing order\n5. delete order")
        user_input_for_order = input("Please choose the id of what's next: ")
        print("-" * 80)
        if user_input_for_order == "0":
            break
        elif user_input_for_order == "1":
            fetch_from_db.print_orders_list()
            print("-" * 80)
        elif user_input_for_order == "2":
            fetch_from_db.create_order()
        elif user_input_for_order == "3":
            fetch_from_db.update_status_in_order_table()
        elif user_input_for_order == "4":
            fetch_from_db.update_order()
        elif user_input_for_order == "5":
            fetch_from_db.delete_order_list()
        else:
            print(f"{user_input_for_order} is not valid. Please try again.")
            print("-" * 80)

    if user_input_for_main_menu != "0" and user_input_for_main_menu != "1" \
            and user_input_for_main_menu != "2" and user_input_for_main_menu != "3":
        print(f"{user_input_for_main_menu} is not valid. Please try again.")
        print("-" * 80)