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
    buy_date: Optional[date] = None    
    sell_date: Optional[date] = None
    sell_price: Optional[float] = None

    # this function saves the products to the csv file
    def save_to_csv(self, filename: str):
        data = asdict(self)
        for key in data.keys():
            if 'date' in key and data[key] is not None:
                data[key] = data[key].strftime('%Y-%m-%d')

        with open(f'{filename}.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())

            # Checks if the file is empty and writes header if needed
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(data)

    # this function returns the sell method
    def sell(self):      
        self.save_to_csv('sales')

     # this function returns the buy method
    @classmethod
    def buy(cls, name, buy_price, expiration_date,  buy_date=None):
        product_id = uuid.uuid4() # generate a new UUID
        buy_date = buy_date or datetime.now().date()
        return cls(product_id=product_id, name=name, buy_price=buy_price, expiration_date=expiration_date, buy_date=buy_date)

    @staticmethod
    def load_data_into_dataframe(filename: str):
        try:
            columns = [
                'Name', 'Buy Price', 'Expiration Date', 'Product ID', 'Buy Date', 'Sell Date', 'Sell Price'
            ]
            date_columns = ['Buy Date', 'Expiration Date', 'Sell Date']
            df = pd.read_csv(f'{filename}.csv',
                            names=columns,
                            header=0,
                            index_col='Product ID'
            )
            for date in date_columns:
                df[date] = pd.to_datetime(df[date], format='%Y-%m-%d').dt.date
            return df
        except FileNotFoundError:
            print("CSV file not found. Returning an empty DataFrame.")
            return pd.DataFrame()