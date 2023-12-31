# Imports
import argparse
from datetime import datetime, timedelta
import os
import sys
# Internal imports
from manager import buy, sell, report_ledger, report_inventory, report_revenue, report_profit, save_current_date_to_file, load_current_date_from_file, list_products, to_json

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "main"

# function to export a json file
def export_to_json(args):
    to_json(args)

# functions for report
def report(args):
    if args.report_type == 'ledger':
        report_ledger(args)
    elif args.report_type == 'inventory':
        report_inventory(args)    
    elif args.report_type == 'revenue':
        report_revenue(args)
    elif args.report_type == 'profit':
        report_profit(args)

def current_date(args):
    try:
        today = datetime.strptime(args.current_date, '%Y-%m-%d').date()
        save_current_date_to_file(args.current_date)
    except ValueError:
        print("Invalid date format. Please use 'YYYY-MM-DD'.")
        sys.exit(1) # exit with an error code

def advance_time(args):
    # advance the current date by the specified number of days and save it to the file
    try:
        loaded_date = load_current_date_from_file()
        new_date = loaded_date + timedelta(days=args.advance_time)
        save_current_date_to_file(new_date.strftime('%Y-%m-%d'))
        print(f"Current date advanced by {args.advance_time} days to {new_date.strftime('%Y-%m-%d')}.")
    except ValueError:
        print("Invalid date stored in file. Please use 'YYYY-MM-DD'.")
        sys.exit(1) # exit with an error code

# superpy main 
def main():
    parser = argparse.ArgumentParser(prog='superpy', description='Welcome to SuperPy - I am here to help you manage your inventory.')
    
    # adding argument directly to parser
    parser.add_argument('--advance_time', type=int, help='Number of days to advance')
    parser.set_defaults(func=advance_time)

    subparsers = parser.add_subparsers(help='Subcommands', dest='command')

    # subparser for buying a product
    buy_parser = subparsers.add_parser('buy', help='Buy a product.')
    buy_parser.add_argument('--name', required=True, help='Product name')
    buy_parser.add_argument('--buy_date', type=str, help="Product buy date (format: YYYY-MM-DD)")
    buy_parser.add_argument('--buy_price', type=float, required=True, help='Product buy price')
    buy_parser.add_argument('--expiration_date', required=True, help='Product expiration date (format: YYYY-MM-DD)')
    buy_parser.set_defaults(func=buy)

    # subparser for selling a product
    sell_parser = subparsers.add_parser('sell', help='Sell a product')
    sell_parser.add_argument('--id', required=True, help='Id of the product to sell')
    sell_parser.add_argument('--sell_date', type=str, help='Product sell date (format: YYYY-MM-DD)')
    sell_parser.add_argument('--sell_price', type=float, required=True, help='Product sell price')
    sell_parser.set_defaults(func=sell)

    # subparser for reports
    report_parser = subparsers.add_parser('report', help='Generate reports of ledger, inventory, revenue and profit.')
    report_parser.add_argument('report_type', choices=['ledger', 'inventory', 'revenue', 'profit'], help='Type of report to generate')
    report_parser.add_argument('--date', required=False, type=str, help='Time option for reports (YYYY-MM-DD) until current date')
    report_parser.set_defaults(func=report)

    # subparser to set the current date
    set_date_parser = subparsers.add_parser('set_date', help='Set the current date')
    set_date_parser.add_argument('current_date', type=str, help='Set the current date (format: YYYY-MM-DD)')
    set_date_parser.set_defaults(func=current_date)

    # exporting to json format
    export_parser = subparsers.add_parser('export', help='Export the dataframes into json files')
    export_parser.add_argument('data_type', choices=['purchases', 'sales'], help=('Which data do you wish to export: purchases or sales?'))
    export_parser.add_argument('--json', dest='json_path', required=True, help='Export the file to json format.')
    export_parser.set_defaults(func=export_to_json)

    args = parser.parse_args()
    
    # advance time if commanded
    if hasattr(args, 'func'):
        if args.command == 'advance_time':
            advance_time(args)
        else:
            args.func(args)
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()