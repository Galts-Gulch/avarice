Contributing
============

General
-------

-   Please no lines greater than 80 characters.
-   Fork, commit, submit pull request.

Adding exchange support
-----------------------

-   Drop the working python3 api into a folder of the exchange name
    (e.g. bitfinex)
-   Note the exchange addition in genconfig.py for Exchange and APIWait.
-   Add a new guard in exchangelayer.py for the exchange. e.g. elif
    genconfig.Exchange == 'bitfinex':
-   For an example of the following, view the 'okcoin' guarded section
    of exchangelayer.

-   We require the following functions:
-   GetMarketPrice
    -   Takes 'bid', 'ask', or 'last' as an argument. Returns a float
        for either. Self explanatory purpose.
-   OrderExist
    -   Checks if the last order exists, and returns True or False. This
        may require to be done different ways for different APIs.
-   CancelOrderIfExist
    -   Doesn't take an argument, returns None. This may require to be
        done in different ways for different APIs. Checks OrderExist,
        and cancels the order if True. May need to use order id on some
        exchanges.
-   Trade
    -   Takes order, rate, and amount. Returns None. Only initiates the
        trade with the exchange api code.
-   We offer the following options:
-   AdditionalAsync
    -   A list of async coroutines you would like to have run forever
        asynchronously. May be useful depending on the API.
