# Contributing

## General
- Ensure your editor is set to use 4 spaces for tab (smartindent, tabstop=4, shiftwidth=4 in vim)
- Please no lines greater than 75char, with <= 70 preferred (in rare cases, exceeding can aid readability)
- Fork, commit, submit pull request.

## Adding exchange support
- Bring in working python3 api in the following form: <exchange>.py i.e. bitfinex.py.
- Note the exchange addition in genconfig.py for Exchange and APIWait.
- Add a new guard in exchangelayer.py for the exchange. i.e. elif genconfig.Exchange == 'bitfinex':
- For an example of the following, view the 'okcoin' guarded section of exchangelayer. Everything below should also be contained in the new exchange guard.

- We require the following functions:
- GetFree
    - Takes either 'currency' or 'asset' as an argument, returns a float for either. Self explanatory purpose.
- GetFrozen
    - Takes either 'currency' or 'asset' as an argument, returns a float for either. Self explanatory purpose.
- GetTradeAmount
    - Takes either 'currency' or 'asset' as an argument, returns a float for either. Uses GetFree to determine the amount we'll be trading with genconfig.TradeVolume's effect.
- GetMarketPrice
    - Takes either 'bid' or 'ask' as an argument. Returns a float for either. Self explanatory purpose.
- CancelOrderIfExist
    - Doesn't take an argument, returns None. This may require to be done in different ways for different APIs. All it does is check if there are current orders in progress, and cancels them if so. May need an order id on some exchanges.
