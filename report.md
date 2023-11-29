To do this assignment as concise and organized as possible I implemented a couple of extra technical elements that also make the coding experience more enjoyable. Although I might have overshot myself with the difficulty level of these extra's. So quite some things don't work as they should.

### 01. INVENTORY AS SINGLE FILE

I wanted to have the data as a single list, since that is how the information is viewed. When a product is acquired there is certain data assigned to it. In this case specifically: id, name, amount bought, expiration date, price and date of acquisition. When the product is eventually sold, if it doesn't expire beforehand, it's still the same product but it gets additional data assigned to it. Such as amount sold, selling price and selling date. 

Here is where I didn't consider that this probably requires a far more complex code than what I can do right now, since if the all the amount bought isn't also sold in one go the registry won't be complete anymore. In hindsight this was not the most efficient setup to use. 

Since when selling it actually adds a new product with all the bought data, this will then skew all the data for the reports. With more time I would change is into two csv files for bought and sold, and would change the code to accommodate this change.

### 02. DATACLASSES AND STATIC TYPING

I found that dataclasses are very good to simplify the setup of a Class and it's methods. This way the code is easier to read and the class Product is easier to define and refer to in the code. Particularly by using @dataclass then it takes less code to define all the variables of the Product class. 

By staticly typing member variables I can avoid a lot of mistakes whilst building my program and makes everything easier to understand.

Examples:

```
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

```

```
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
```

### 03. PANDAS

I found that returning the data from csv files wasn't easily understandable therefore using pandas seemed like the logical choice. Pandas is also better at managing and doing operations on the data, which seemed ideal for the report calculations. It was quite challenging to find how pandas stores some data and what code implementations are necessary to then be able to manipulate this data. Like the case with dates. The input is in datetime, which then pandas stores as datetime64 dtype in the DataFrame and then has to be converted back into datetime for comparison purposes.
