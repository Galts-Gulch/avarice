# avarice
*(noun) extreme greed for wealth or material gain.*

*Greed captures the essence of the evolutionary spirit.*
-Gordon Gekko

##include std/disclaimer.h
- This software is in a very WIP state.
- Only a few hours was spent on this first push while getting a quick grasp of Python3.
- It is not recommended to live trade at all, and any assets you may lose are your own responsibility.
- All (very minimal) testing is done on current Python3.5.

## TODO
- More indicators
- Implement a few well tested multi-indicator strategies from my c++ trade infrastructure, including bayesian targeted, bfsg optimized spread code (the latter might be done via non python since it's already c++ and I'm lazy)
- Support "Max Trade Slippage" using ADX and asset + currency trade volume, and bollinger bands with bollbandwidth = (PeriodBandHigh - PeriodBandLow) / (PeriodBandSum / Period)
- Clean up a lot
- Record at candle market depth in a new sqlite table, break markets into child markets for better economic significance backtesting (cryptotrader "at market" style backtesting is a joke in the economics world).
- Probably rework into real classes

## Contributing
- Ensure your editor is set to use 4 spaces for tab (smartindent, tabstop=4, shiftwidth=4 in vim)
- Please no lines greater than 75char, with <= 70 preferred (in rare cases, exceeding can aid readability)
- Fork, commit, submit pull request.

## Running
- Be sure you have simplejson, if not install it for python3.y
- Clone
- Edit genconfig.py; find your own successful configuration
- Run avarice.py
