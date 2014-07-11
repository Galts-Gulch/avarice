# Contributing

## General
- Ensure your editor is set to use 4 spaces for tab (smartindent, tabstop=4, shiftwidth=4 in vim)
- Please no lines greater than 75char, with <= 70 preferred (in rare cases, exceeding can aid readability)
- Fork, commit, submit pull request.

## Adding exchange support
- Bring in working python3 api in the following form: <exchange>_api.py i.e. bitfinex_api.py.
- Note the exchange addition in genconfig.py for Exchange and APIWait.
- Add a new guard in exchangelayer.py for the exchange. i.e. elif genconfig.Exchange == 'bitfinex':
- For an example of the following, view the 'okcoin' guarded section of exchangelayer. Everything below should also be contained in the new exchange guard.

- We require the following functions:
- GetTradeAmount
    - Takes either 'currency' or 'asset' as an argument, returns a float for either. Uses GetFree (if implemented this way) to determine the amount we'll be trading with genconfig.TradeVolume's effect.
- GetMarketPrice
    - Takes either 'bid' or 'ask' as an argument. Returns a float for either. Self explanatory purpose.
- OrderExist
    - Checks if the last order exists, and returns True or False. This may require to be done different ways for different APIs.
- CancelOrderIfExist
    - Doesn't take an argument, returns None. This may require to be done in different ways for different APIs. Checks OrderExist, and cancels the order if True. May need to use order id on some exchanges.
- Trade
    - Takes order, rate, amount, and pair as arguments, and returns None. Only initiates the trade with the exchange api code.
