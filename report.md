To do this assignment as concise and organized as possible I implemented a couple of extra technical elements which also make the coding experience more enjoyable. Although I might have overshot myself with the difficulty level of these extra's (namely pandas and dataclasses) and ended up having to keep the functionality of the CLI quite simple to be able to finish the assignment within the given timeframe.

### 01. MANAGING THE CSV FILES

When setting up the csv files with the product data, instead of having two separate files about the same product but with separate data other than the unique id number, I created the class *Product* already with the sale columns which stay empty in the *purchases.csv* file. Until the product is sold, then pandas will take the data from the *purchases.csv* and write it in the *sales.csv* with the added sales data. 

Examples of the data in the csv files:

**Purchases.csv** 
```
name,buy_price,expiration_date,product_id,buy_date,sell_date,sell_price
banana,1.0,2023-11-12,99aaa2cd-b20f-49fe-8706-b60a9a7fd397,2023-11-05,,
```

**Sales.csv**

```
name,buy_price,expiration_date,product_id,buy_date,sell_date,sell_price
banana,1.0,2023-11-12,99aaa2cd-b20f-49fe-8706-b60a9a7fd397,2023-11-05,2023-11-10,2.0
```
This in return made it easier to make the calculations for the reports, as seen in the example below:

```
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

```

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
    buy_date: Optional[date] = None    
    sell_date: Optional[date] = None
    sell_price: Optional[float] = None

```

### 03. PANDAS

I found that returning the data from csv files wasn't easily understandable therefore using pandas seemed like the logical choice. Pandas is also better at managing and doing operations on the data, which seemed ideal for the report calculations. It was quite challenging to find how pandas stores some data and what code implementations are necessary to then be able to manipulate this data. Like the case with dates. The input is in datetime, which then pandas stores as datetime64 dtype in the DataFrame and then has to be converted back into datetime for comparison purposes.

The advantage is that pandas already has a lot of integrated features to manage and display data, so it's worth the struggle to learn it.