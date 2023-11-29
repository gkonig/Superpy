Welcome to Superpy

All commands are operated with the command line. In this file you can find the commands you can use.
They are organised under four different categories, such as:

Buying products

    With the 'buy' command you can buy products and add them to the inventory.
    After the 'buy' command you can use the following subcommands for data input:
        '--name'            Name of the product. Use underscore instead of space between words.
        '--buy_amount'      Amount of products bought with the sme attributes. 
        '--buy_date'        Date of when the product was acquired. Format has to be YYYY-MM-DD. Defaults to current date if there is no input.
        '--buy_price'       Price for which the product was acquired. Input a number, can have a decimal.
    	'--expiration_date' Expiration date of the product. Format has to be YYYY-MM-DD.
    
    All items with the same attributes will be given a unique id number.

    Example of commands:

    python super.py buy --name papaya --buy_amount 20 --buy_date