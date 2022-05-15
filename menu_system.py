import pandas as pd

product_list = pd.read_csv('products.csv').to_dict()
main_menu_option = ["Please choose what you want to do next:\n"
                    "0. SAVE & EXIT",
                    "1. check product menu",
                    "2. check courier options",
                    "3. your order",
                    ]
