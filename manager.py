# Imports
from datetime import datetime, timedelta, date
from Product import Product
import pandas as pd

# functions for reading and writing the current date
DATE_FILE_PATH = 'current_date.txt'

# function to buy a product
def buy(args):
    expiration_date = datetime.strptime(args.expiration_date, '%Y-%m-%d').date()
    buy_date = datetime.strptime(args.buy_date, '%Y-%m-%d').date() if args.buy_date else datetime.now().date()
    product = Product.buy(args.name, args.buy_price, expiration_date, args.buy_amount, buy_date)
    product.save_to_csv()

# function to sell a product
def sell(args):
    df = Product.load_data_into_dataframe()
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
        buy_amount=product['Buy Amount'],
        sell_amount=args.sell_amount,
        buy_date=product['Buy Date'],
        sell_date=sell_date,
        sell_price=args.sell_price
        )
    product_obj.sell()

# function to list all products in inventory
def list_products(args):
    df = Product.load_data_into_dataframe()
    print(df)

# function to report all expired products
def report_expired_products(args):
    df = Product.load_data_into_dataframe()
    current_date = args.current_date if args.current_date else datetime.now().date()
    
    if args.time_option:
        now = datetime.date.today()
        if args.time_option == 'yesterday':
            expired_products = df[df['Expiration date'] < current_date - timedelta(days=1)]
        elif args.time_option == 'now':
            expired_products = df[df['Expiration date'] < current_date]
        elif args.time_option == 'tomorrow':
            expired_products = df[df['Expiration date'] < current_date + timedelta(days=1)]
        elif args.time_option.startswith('between'):
            start, end = map(datetime.strptime.strptime, args.time_option.split(' ')[1:], ['%Y-%m-%d', '%Y-%m-%d'])
            expired_products = df[(df['Expiration date'] >= start.date()) & (df['Expiration date'] <= end.date())]
    
    else:
        expired_products = df[df['Expiration date'] < current_date]
    
    if expired_products.empty:
        print("There are no expired products.")
    else:
        print("The following products have expired:")
        print(expired_products[['Name', 'Amount bought', 'Expiration date']])
    
# function to report inventory
def report_inventory(args):
    df = Product.load_data_into_dataframe()
    print("Current inventory:")
    print(df.fillna('-'))

# function to report revenue
def report_revenue(args):
    input_date = datetime.strptime(args.date, '%Y-%m-%d').date() if args.date else pd.Timestamp.min
    total_revenue = calculate_revenue(input_date)
    print(f'Total revenue is: {total_revenue}')

# function to report profit
def report_profit(args):
    input_date = datetime.strptime(args.date, '%Y-%m-%d').date() if args.date else pd.Timestamp.min
    total_profit = (calculate_revenue(input_date) - calculate_loss(input_date))
    print(f'Total profit is: {total_profit}')

def save_current_date_to_file(current_date) -> None:
    with open(DATE_FILE_PATH, 'w') as file:
        file.write(current_date)

def load_current_date_from_file() -> date:
    try:
        with open(DATE_FILE_PATH, 'r') as file:
            return datetime.strptime(file.read().strip(), '%Y-%m-%d').date()
    except FileNotFoundError:
        return None
    

def calculate_revenue(initial_date):
    sold_inventory_df = Product.load_data_into_dataframe()[['Sell Date', 'Sell Price']].dropna()
    loaded_date = load_current_date_from_file()
    current_date = loaded_date if loaded_date else datetime.now().date()
    if sold_inventory_df.empty:
        total_revenue = 0
    else:
        dated_sold_inventory_df = sold_inventory_df[
            (
                sold_inventory_df['Sell Date'] > pd.to_datetime(initial_date)
            ) & (
                sold_inventory_df['Sell Date'] < pd.to_datetime(current_date)
            )
            ]
        total_revenue = dated_sold_inventory_df['Sell Price'].sum()
    return total_revenue

def calculate_loss(initial_date):
    bought_inventory_df = Product.load_data_into_dataframe()[['Buy Date', 'Buy Price']].dropna()
    loaded_date = load_current_date_from_file()
    current_date = loaded_date if loaded_date else datetime.now().date()
    if bought_inventory_df.empty:
        total_loss = 0
    else:
        dated_sold_inventory_df = bought_inventory_df[
            (
                bought_inventory_df['Buy Date'] > pd.to_datetime(initial_date)
            ) & (
                bought_inventory_df['Buy Date'] < pd.to_datetime(current_date)
            )
            ]
        total_loss = dated_sold_inventory_df['Buy Price'].sum()
    return total_loss