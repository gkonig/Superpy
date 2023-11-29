# Imports
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from typing import Optional
import uuid
from uuid import UUID
import csv
import pandas as pd

# This class defines the product for selling and buying
@dataclass
class Product:
    name: str
    buy_price: float
    expiration_date: date
    product_id: UUID = field(default_factory=UUID)    
    buy_amount: int = 1 # quantity of products bought / to buy
    sell_amount: Optional[int] = None# quantity of products sold / to sell
    buy_date: Optional[date] = None    
    sell_date: Optional[date] = None
    sell_price: Optional[float] = None

    # this function saves the products to the csv file
    def save_to_csv(self):
        data = asdict(self)
        print(data)
        data['buy_date'] = data['buy_date'].strftime('%Y-%m-%d')
        data['expiration_date'] = data['expiration_date'].strftime('%Y-%m-%d')
        if data['sell_date']:
            data['sell_date'] = data['sell_date'].strftime('%Y-%m-%d')

        with open('inventory.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())

            # Checks if the file is empty and writes header if needed
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(data)

    # this function returns the sell method
    def sell(self):

        if self.sell_amount > self.buy_amount:
            raise ValueError ("Cannot sell more than available in inventory.")
        
        self.save_to_csv()

     # this function returns the buy method
    @classmethod
    def buy(cls, name, buy_price, expiration_date,  buy_amount=1, buy_date=None):
        product_id = uuid.uuid4() # generate a new UUID
        buy_date = buy_date or datetime.now().date()
        return cls(product_id=product_id, name=name, buy_price=buy_price, expiration_date=expiration_date, buy_amount=buy_amount, buy_date=buy_date)

    @staticmethod
    def load_data_into_dataframe():
        try:
            columns = [
                'Name', 'Buy Price', 'Expiration Date', 'Product ID', 'Buy Amount', 'Sell Amount', 'Buy Date', 'Sell Date', 'Sell Price'
            ]
            date_columns = [
                ['Buy Date', 'Expiration Date', 'Sell Date']
            ]
            df = pd.read_csv('inventory.csv',
                            names=columns, 
                            header=0, 
                            index_col='Product ID'
            )
            df[['Buy Date', 'Expiration Date', 'Sell Date']] = df[['Buy Date', 'Expiration Date', 'Sell Date']].apply(pd.to_datetime)
            return df
        except FileNotFoundError:
            print("CSV file not found. Returning an empty DataFrame.")
            return pd.DataFrame()