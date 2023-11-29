Welcome to Superpy

All commands are operated with the command line. In this file you can find the commands you can use.
They are organised under four different categories, such as:

Buying products

    With the 'buy' command you can buy products and add them to the inventory.
    After the 'buy' command you can use the following subcommands for data input:
        '--name'            Name of the product. Use underscore instead of space between words.
        '--buy_amount'      Amount of products bought with the same attributes. 
        '--buy_date'        Date of when the product was acquired. Format has to be YYYY-MM-DD. Defaults to current date if there is no input.
        '--buy_price'       Price for which the product was acquired. Input a number, can have a decimal.
    	'--expiration_date' Expiration date of the product. Format has to be YYYY-MM-DD.
    
    All items with the same attributes will be given a unique id number.

    Example:

        python super.py buy --name orange --buy_amount 20 --buy_date 2023-11-28 --buy_price 1 --expiration_date 2023-12-01

    The data will be stored in inventory.csv.

Selling products

    With the 'sell' command you can sell products and record it to the inventory.
    After the 'sell' command you can use the following subcommands for data input:
        '--id'               Id of the product to sell. This is long number, so copy-paste is advised.
        '--sell_amount'      Amount of products self with the same attributes. This amount can never be higher than the amount bought.
        '--sell_date'        Date of when the product was sold. Format has to be YYYY-MM-DD. Defaults to current date if there is no input.
        '--sell_price'       Price for which the product was sold. Input a number, can have a decimal.
    
    Example:

        python super.py sell --id 718fca8b-c6cd-4a87-abab-515a26b869d0 --sell_amount 20 --sell_date 2023-11-29 --sell_price 2.2

    The data will be stored in inventory.csv next to the columns of the respective bought product.

Setting the time:

    In current_date.txt the current is stored. This can be changed.
    
    You can change the current date with the following optional commands:
        '--set_date'        With this command you can set the current date manually in format YYYY-MM-DD.
        '--advance_time'    Follow the command with the amount of days you which to advance.
    
    For example, if the current date should be the 15th of December of 2023 then:

        python super.py set_date 2023-12-15

    And if time should be advanced by 2 days:

        python super.py --advance_time 2
    
Reports:

    With 'report' it's possible to get different types of reports. 
    The choices are 'expired', 'inventory', 'revenue' and 'profit'.

        'expired'           Returns a list of expired products.
        'inventory'         Returns a list of all expired products.
        'revenue'           Returns the revenue.
        'profit'            Returns the profit.

    For these reports a date should be specifief with the command '--date'.

        '--date'            Follow the command with a date in format YYYY-MM-DD.

    Example:

        python super.py expired --date

Additional guidance commands:

    python super.py -h
    python super.py buy --help
    python super.py report revenue --help