# Imports
from datetime import datetime, timedelta, date
from Product import Product
import pandas as pd
import tabulate as tb

# functions for reading and writing the current date
DATE_FILE_PATH = 'current_date.txt'

# function to buy a product
def buy(args):
    expiration_date = datetime.strptime(args.expiration_date, '%Y-%m-%d').date()
    buy_date = datetime.strptime(args.buy_date, '%Y-%m-%d').date() if args.buy_date else datetime.now().date()
    product = Product.buy(args.name, args.buy_price, expiration_date, buy_date)
    product.save_to_csv('purchases')
    print(f'Purchase sucessfull.')

# function to sell a product
def sell(args):
    df = Product.load_data_into_dataframe('purchases')
    if args.id not in df.index:
        print(f'Product with ID {args.id} not found.')
        return

    product = df.loc[args.id]
    if not pd.isnull(product['Sell Date']):
        print(f'Product with ID {args.id} has already been sold.')
        return
    
    sell_date = datetime.strptime(args.sell_date, '%Y-%m-%d').date() if args.sell_date else datetime.now().date()

    product_obj = Product(
        name=product['Name'], 
        buy_price=product['Buy Price'], 
        expiration_date=product['Expiration Date'],
        product_id=args.id,
        buy_date=product['Buy Date'],
        sell_date=sell_date,
        sell_price=args.sell_price
        )
    product_obj.sell()
    print(f'Product sold sucessfully.')

# function to list all products
def list_products(args):
    purchases = Product.load_data_into_dataframe('purchases')
    sales = Product.load_data_into_dataframe('sales')

# function to report the current ledger
def report_ledger(args):
    purchases = Product.load_data_into_dataframe('purchases')
    sales = Product.load_data_into_dataframe('sales')
    ledger = pd.concat([purchases, sales], axis=0)
    ledger = ledger.fillna('-')
    print("Current ledger:")
    print(ledger.to_markdown(tablefmt="pretty"))

# function to report inventory
def report_inventory(args):
    purchases = Product.load_data_into_dataframe('purchases')
    sales = Product.load_data_into_dataframe('sales')
    sold_ids = sales.index.values.tolist()
    inventory = purchases[~purchases.index.isin(sold_ids)]
    inventory = inventory.fillna('-')
    inventory['Expiration Date'] = pd.to_datetime(inventory['Expiration Date'], errors='coerce').dt.date
    loaded_date = load_current_date_from_file()
    inventory['Expired'] = inventory['Expiration Date'] <= loaded_date
    inventory['Expired'] = inventory['Expired'].map({True: 'YES', False: 'NO'})
    print("Current inventory:")
    print(inventory.to_markdown(tablefmt="pretty"))

# function to report revenue
def report_revenue(args):
    input_date = datetime.strptime(args.date, '%Y-%m-%d').date() if args.date else pd.Timestamp.min
    total_revenue = calculate_revenue(input_date)
    print(f'Total revenue is: {round(total_revenue,2)}')

# function to report profit
def report_profit(args):
    input_date = datetime.strptime(args.date, '%Y-%m-%d').date() if args.date else pd.Timestamp.min
    total_profit = (calculate_revenue(input_date) - calculate_loss(input_date))
    print(f'Total profit is: {round(total_profit,2)}')

# function to export the sales dataframe to json
def to_json(args):
    try:
        data_type = args.data_type
        json_filename = args.json_path
        data = Product.load_data_into_dataframe(data_type)
        data.to_json(json_filename, orient='records', date_format='iso')
        print(f"The file {json_filename} has been exported with the {data_type} data.")
    except Exception as e:
        print('An error occured while trying to export data.')

# function to save the current date to the file
def save_current_date_to_file(current_date) -> None:
    with open(DATE_FILE_PATH, 'w') as file:
        file.write(current_date)

# function to load the current date from the file
def load_current_date_from_file() -> date:
    try:
        with open(DATE_FILE_PATH, 'r') as file:
            return datetime.strptime(file.read().strip(), '%Y-%m-%d').date()
    except FileNotFoundError:
        return None
    
# function to calculate the revenue(used in revenue and profit)
def calculate_revenue(initial_date):
    sold_inventory_df = Product.load_data_into_dataframe('sales')[['Sell Date', 'Sell Price']].dropna()
    loaded_date = load_current_date_from_file()
    current_date = loaded_date if loaded_date else datetime.now().date()
    if sold_inventory_df.empty:
        total_revenue = 0
    else:
        dated_sold_inventory_df = sold_inventory_df[
            (
                sold_inventory_df['Sell Date'] > pd.to_datetime(initial_date).date()
            ) & (
                sold_inventory_df['Sell Date'] < pd.to_datetime(current_date).date()
            )
            ]
        total_revenue = dated_sold_inventory_df['Sell Price'].sum()
    return total_revenue

# function to claculate the loss (used in profit)
def calculate_loss(initial_date):
    bought_inventory_df = Product.load_data_into_dataframe('purchases')[['Buy Date', 'Buy Price']].dropna()
    loaded_date = load_current_date_from_file()
    current_date = loaded_date if loaded_date else datetime.now().date()
    if bought_inventory_df.empty:
        total_loss = 0
    else:
        dated_sold_inventory_df = bought_inventory_df[
            (
                bought_inventory_df['Buy Date'] > pd.to_datetime(initial_date).date()
            ) & (
                bought_inventory_df['Buy Date'] < pd.to_datetime(current_date).date()
            )
            ]
        total_loss = dated_sold_inventory_df['Buy Price'].sum()
    return total_loss
