# Imports
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from typing import Optional
import uuid
from uuid import UUID
import csv
import pandas as pd

# This class is to generate a unique ID to the product
#class IdGenerator:
    #_counter = 0
#
    #@classmethod
    #def generate_id(cls):
        #cls._counter +- 1
        #return cls._counter

# This class defines the product for selling and buying
@dataclass
class Product:
    name: str
    buy_price: float
    expiration_date: date
    product_id: UUID = field(default_factory=UUID)    
    buy_amount: int = 1 # quantity of products bought / to buy
    sell_amount: Optional[int] = 0 # quantity of products sold / to sell
    buy_date: Optional[date] = None    
    sell_date: Optional[date] = None
    sell_price: Optional[float] = None

    # this function returns the revenue attribute
    @property
    def revenue(self):
        if self.sell_price is not None:
            return self.sell_price * self.sell_amount
        return 0.0
    
     # this function returns the profit attribute
    @property
    def profit(self):
        if self.sell_price is not None:
            return (self.sell_price - self.buy_price) * min(self.sell_amount, self.buy_amount)
        return 0.0

    # this function saves the products to the csv file
    def save_to_csv(self):
        data = asdict(self)
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
    def sell(self, sell_price, sell_amount=1, sell_date=None):
        sell_date = sell_date or datetime.now().date()

        if  sell_amount > self.buy_amount:
            raise ValueError ("Cannot sell more than available in inventory.")
        
        self.sell_amount += sell_amount
        self.buy_amount -= sell_amount # Update the buy_amount accordingly
        self.sell_date = sell_date
        self.sell_price = sell_price
        self.save_to_csv()

     # this function returns the buy method
    @classmethod
    def buy(cls, name, buy_price, expiration_date,  buy_amount=1, buy_date=None):
        product_id = uuid.uuid4() # generate a new UUID
        buy_date = buy_date or datetime.now().date()
        return cls(product_id, name, buy_price, expiration_date, buy_amount=buy_amount, buy_date=buy_date)

    @staticmethod
    def load_data_into_dataframe():
        try:
            df = pd.read_csv('products.csv', 
                             parse_dates=['buy_date', 'expiration_date'], 
                             names=['ID', 'Name', 'Buy_amount', 'Buy date', 'Buy price', 'Expiration date', 'Sell_amount', 'Sell date', 'Sell price'], 
                             header=1, 
                             index_col='ID')
            return df
        except FileNotFoundError:
            print("CSV file not found. Returning an empty DataFrame.")
            return pd.DataFrame()