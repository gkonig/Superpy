# Imports
from datetime import datetime, timedelta
from Product import Product
import pandas as pd

# function to buy a product
def buy(args):
    expiration_date = datetime.strptime(args.expiration_date, '%Y-%m-%d').date()
    buy_date = datetime.strptime(args.buy_date, '%Y-%m-%d').date() if args.buy_date else datetime.now().date()
    product = Product.buy(args.name, args.buy_amount, buy_date, args.buy_price, expiration_date)
    product.save_to_csv()

# function to sell a product
def sell(args):
    df = Product.load_data_into_dataframe()
    if args.id not in df.index:
        print(f'Product with ID {args.id} not found.')
        return

    product = df.loc[args.id]
    if not pd.isnull(product['Sell date']):
        print(f'Product with ID {args.id} has already been sold.')
        return
    
    sell_date = datetime.strptime(args.sell_date, '%Y-%m-%d').date() if args.sell_date else datetime.now().date()
    product_obj = Product(product.name, product['Buy price'], product['Expiration date'])
    product_obj.product_id = args.id
    product_obj.sell(args.sell_amount, sell_date, args.sell_price)

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
    print(df[['Name', 'Amount bought', 'Buy date', 'Buy price', 'Expiration date', 'Amount sold', 'Sell date', 'Sell price']].fillna('-'))

# function to report revenue
def report_revenue(args):
    df = Product.load_data_into_dataframe()
    current_date = args.current_date if args.current_date else datetime.now().date()

    total_revenue = df['Sell price'].sum()
    print(f'Total revenue is: {total_revenue}')

# function to report profit
def report_profit(args):
    df = Product.load_data_into_dataframe()
    current_date = args.current_date if args.current_date else datetime.now().date()

    total_profit = (df['Sell price'] - df['Buy price']).sum()
    print(f'Total profit is: {total_profit}')