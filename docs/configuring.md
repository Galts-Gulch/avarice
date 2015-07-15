Configuring
===========

All configuration is accomplished by editing config.ini or running python3 webconfigure.py and visiting 127.0.0.1:5000 in a web browser.

API
---

-   **Exchange:** OKCoin exchanges are only supported at this time. To switch between the CN and INTL exchange, change Trade Pair.
-   **Trade Pair:** Asset and currency to trade in. cny pairs use
    okcoin.cn and usd pairs switch to okcoin.com.
-   **API Key:** Only used if Trader is enabled (not used if only
    simulating).
-   **Secret Key:** Only used if Trader is enabled (not used if only
    simulating).
-   **Asset Trade Minimum:** The minimum allowed asset trade size. This is generally 0.01 for BTC and 0.1 for LTC on OKCoin.

Candles
-------

-   **Verbose:** Should each candle print additional information such as candle number, price, time, and date?
-   **Size:** Candle Size in minutes. This is used for all indicator
    assessments, and trade frequency.

Trader
------

-   **Enabled:** Should we live trade with real money? This always
    sells/buys at market bid/ask.
-   **Everything below is also used by simulator:**
-   **Trade Indicators:** [indicators](indicators.md) has info on separately configuring each indicator.
    -   You may set multiple indicators to be traded by using a list
        format.
    -   A nested list means that those indicators should be combined (so
        signals from both should match before trading). These use
        Trade Volume, Single Trade, Trade Persist, and Trade Delay from this
        top level Trader class.
    -   A top level list entry means that indicator will be traded
        independently and use it's own Trader values (set in an indicator's "Trader" section further down in the config, or on the indicator page in web configure).
    -   Any volatility indicator must be used in a combined list to
        function since they don't generate signals on their own.
    -   Some indicators may be referenced with a concise or expanded name such as "EMA" and "Exponential Movement Average". The names are interchangeable.
    -   Below are some examples of configurations with descriptions:
        -   Only trade if EMA and MACD signals match, and also trade
            FullStochRSID independent of any other Trade Indicators:

                Trade Indicators = [['EMA', 'MACD'], 'FullStochRSID']

        -   Only trade if EMA and MACD signals match:

                Trade Indicators = [['EMA', 'MACD']]

        -   Trade EMA and FullStochRSID independently of one another:

                Trade Indicators = ['EMA', 'FullStochRSID']

        -   Only trade EMA:

                Trade Indicators = ['EMA']

        -   Only trade MACD if BollBandwidth is beyond it's Threshold:

                Trade Indicators = [['BollBandwidth', 'MACD']]

-   **Advanced Strategy:** This is an advanced option with no other
    available option in the stock Avarice package. This may be changed to the function name of a custom written strategy in strategies.py.
-   **Verbose:** This may be set to True or False, or checked/unchecked. Should we print additional information about the indicator on each candle?
-   **Candle Size Multiplier:** Whole numbers only, used for aggregation. E.g. set to 3 if on 5 min candles and 15min indicator period is desired. A more advanced feature to offer per-indicator fine-tuning.
-   **Trade Volume:** Percentage of available asset and currency
    evaluated on each trade. 50 is 50%. Only used on combined
    indicators. It is recommended to set this to a low value if
    Single Trade is not enabled.
-   **Single Trade:** Should we only do a single sell or buy?
    This still uses Trade Volume percent on each trade. This is useful
    for MA style strategies, whereas oscillator or diff style should be
    set to False (to often continue selling if above threshold, or
    buying below).
-   **Trade Delay:** How many candles with indicator info before allowing trades? *Must be equal to 1.*
-   **ReIssue Slippage:** What delta (as a percentage) of order price
    should we continue trying to get an order through for?
-   **ReIssue Delay:** How many seconds should we wait for an order to
    succeed before attempting to re-order? *This also affects the order
    delay*
-   **Volatility Threshold Over:** Only available on volatility
    indicators. This is default enabled, and runs if the volatility
    indicator is above threshold. This may be set to *False* to reverse
    the behavior.

Simulator
---------

-   **Verbose**: Simulate trades using our paper trader. *Always
    simulates sells/buys at market bid/ask*
-   **Asset:** Number of BTC or LTC to start the simulation with.
-   **Currency:** Number of CNY or USD to start the simulation with.

Notifier
--------

-   **Text File:** Record a log of all simulator and trader actions.
    -   **Rollover Time:** Time in hours to switch to a new log file.
    -   **Backup Count:** How many log files to keep? 0 to keep all.
    -   **Path:** Relative path to simulator and trader text file
        directory.
    -   **Trader File Name:** Filename for trader text file.
    -   **Simulator File Name:** Filename for simulator text file.
-   **Pushover:** Push notifications to your
    [Pushover](https://pushover.net/) account.
    -   **Simulator:** Enable for simulator actions.
    -   **Trader:** Enable for trader actions.
    -   **App Token:** The Pushover *Application Token* to be used.
        Register a new app [here](https://pushover.net/apps/build)
    -   **User Key:** Your Pushover *User Key* found on the Pushover
        dashboard.
-   **SMTP:** Non-TLS SMTP email support.
    -   **Simulator:** Enable for simulator actions.
    -   **Trader:** Enable for trader actions.
    -   **Host:** SMTP host to be used.
    -   **From:** SMTP account to send from.
    -   **To:** Email address to send to.
-   **TLS SMTP:** TLS SMTP email support. Configured for GMail by
    default.
    -   **Simulator:** Enable for simulator actions.
    -   **Trader:** Enable for trader actions.
    -   **Host:** TLS SMTP host to be used. *smtp.gmail.com* by default
        for GMail.
    -   **Port:** TLS SMTP port to be used. *587* by default for GMail.
    -   **Username:** TLS SMTP username to be used. For GMail creating a
        new account is recommended. You will need to login to your new
        GMail account and [enable access for less secure
        apps](https://www.google.com/settings/security/lesssecureapps).
    -   **Password:** Your TLS SMTP account password.
    -   **To:** Email address to send to.

Database
--------

-   **Archive:** Save all data in Archive.sqlite in database Path.
-   **Store All:** Never delete any data. Avarice normally only keeps the needed data.
-   **Debug:** Debug flag avoids dropping the db table. *This is only
    ever used for developing and should not otherwise be used.*
-   **Path:** Relative path to database directory.

Grapher
-------

-   **Enabled:** Support recording graphs. *Requires pygal and lxml to
    function correctly.*
-   **Path:** Relative path to chart directory.
-   **Theme:** Choose one of the following:

    > LightSolarized, Light, Clean, Red Blue, DarkColorized,
    > LightColorized, Turquoise, LightGreen, DarkGreen, DarkGreenBlue,
    > Blue.

-   **Indicators:** A list of indicators to graph. Example:

        Indicators = ['MACD', 'EMA']

-   **Show Time:** Show time or show candle numbers as x axis labels?
-   **Max Lookback:** How many candles should we show on the graph
    (x-axis)?

Indicators
----------

-   Any **Trader** nested config only effects
    the indicator if it's an independent indicator (not a combined
    indicator). See the "Trade Indicator" section above in documentation
    for more info.
-   **Verbose:** This may be set to True or False, or checked/unchecked. Should we print additional information about the indicator on each candle?
-   **Candle Size Multiplier:** Whole numbers only, used for aggregation. E.g. set to 3 if on 5 min candles and 15min indicator period is desired. A more advanced feature to offer per-indicator fine-tuning.
-   **Trade Volume:** Percentage of available asset and currency
        evaluated on each trade. 50 is 50%. Only used on combined
        indicators. It is recommended to set this to a low value if
        Single Trade is not enabled.
-   **Single Trade:** Should we only do a single sell or buy?
        This still uses Trade Volume percent on each trade. This is useful
        for MA style strategies, whereas oscillator or diff style should be
        set to False (to often continue selling if above threshold, or
        buying below).
-   **Trade Delay:** How many candles with indicator info before allowing trades? *Must be equal to 1.*
-   **Volatility Threshold Over:** Only available on volatility
        indicators. This is default enabled, and runs if the volatility
        indicator is above threshold. This may be set to *False* to reverse
        the behavior.
-   All indicators are detailed in the [Indicators](indicators.md) page.
