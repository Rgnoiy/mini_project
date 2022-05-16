import pandas as pd

product_list = pd.read_csv('products.csv')

while True:
    user_input = input(
        "Please choose what you want to do next:\n0. SAVE & EXIT\n1. check product menu\n2. check courier options\n3. your order"
    )
    if user_input == "1":
        print(product_list)
    else:
        break