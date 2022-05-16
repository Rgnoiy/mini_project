import pandas as pd

product_list = pd.read_csv('products.csv')

while True:
    print("Main Menu\n0. SAVE & EXIT\n1. product\n2. courier\n3. order")
    user_input_for_main_menu = input("Please choose what's next: ")     # TODO: exception handling
    print("-" * 50)
    while user_input_for_main_menu == "1":
        print("Product Menu\n0. return to main menu\n1. check product menu\n2. add new product to menu\n3. Update existing product\n4. delete product")
        user_input_for_product = input("Please choose what's next: ")       # TODO: exception handling
        print("-" * 50)
        if user_input_for_product == "0":
            break
        elif user_input_for_product == "1":
            product_list = pd.read_csv('products.csv')
            print(product_list)
            print("-" * 50)
            continue
        elif user_input_for_product == "2":
            print("You are adding new product to the menu.")
            product = input("product name: ")  # is it ok to insert only one data set at a time?# TODO: exception handling
            price = input(f"price for {product}: ")      # TODO: exception handling
            new_product_and_price = pd.DataFrame({
                                                  'product': [f'{product}'],
                                                  'price': [f'{price}']
                                                  })
            new_product_and_price.to_csv('products.csv', mode='a', index=False, header=False)

    else:
        break