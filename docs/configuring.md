Configuring
===========

All configuration is accomplished by editing genconfig.py

API
---

-   **Exchange:** OKCoin exchanges are only supported at this time
-   **TradePair:** Asset and currency to trade in. cny pairs use
    okcoin.cn and usd pairs switch to okcoin.com
-   **Asset:** Should not be modified
-   **Currency:** Should not be modified
-   **apikey:** Only used if Trader is enabled (not used if only
    simulating). Must be surrounded by apostrophes.
-   **secretkey:** Only used if Trader is enabled (not used if only
    simulating). Must be surrounded by apostrophes.
-   **AssetTradeMin:** The minimum allowed asset trade size. This is
    0.01 for BTC and 0.1 for LTC on OKCoin.

Candles
-------

-   **Verbose:** Should each candle be printed with the number, last
    price, time, and date?
-   **Size:** Candle Size in minutes. This is used for all indicator
    assessments, and trade frequency.

Trader
------

-   **Enabled:** Should we live trade with real money? This always
    sells/buys at market bid/ask.
-   **Everything below is also used by simulator:**
-   **TradeIndicators:** IndicatorList has all available options, and
    [indicators](indicators.md) has info on configuring each.
    -   You may set multiple indicators to be traded by using a list
        format.
    -   A nested list means that those indicators should be combined (so
        signals from both should match before trading). These use
        TradeVolume, SingleTrade, TradePersist, and TradeDelay from this
        top level Trader class.
    -   A top level list entry means that indicator will be traded
        independently and use it's own Trader values (e.g. set in Class
        EMA: Class Trader:)
    -   Any volatility indicator must be used in a combined list to
        function since they don't generate signals on their own.
    -   Below are some examples of configurations with descriptions:
        -   Only trade if EMA and MACD signals match, and also trade
            FullStochRSID independent of any other TradeIndicators:

                TradeIndicators = [['EMA', 'MACD'], 'FullStochRSID']

        -   Only trade if EMA and MACD signals match:

                TradeIndicators = [['EMA', 'MACD']]

        -   Trade EMA and FullStochRSID independently of one another:

                TradeIndicators = ['EMA', 'FullStochRSID']

        -   Only trade EMA:

                TradeIndicators = ['EMA']

        -   Only trade MACD if BollBandwidth is beyond it's Threshold:

                TradeIndicators = [['BollBandwidth', 'MACD']]

-   **VerboseIndicators:** Indicators which should be verbose each
    candle. By default, we only print trades if all conditions are met.
    Example:

        VerboseIndicators = ['MACD', 'EMA', 'FRAMA']

-   **AdvancedStrategy:** This is an advanced option with no other
    available option stock. This may be changed to the function name of
    a custom written strategy in strategies.py.
-   **TradeVolume:** Percentage of available asset and currency
    evaluated on each trade. 50 is 50%. Only used on combined
    indicators. It is recommended to set this to a low value if
    SingleTrade is enabled.
-   **SingleTrade:** Should we only do a single consecutive sell or buy?
    This still uses TradeVolume percent on each trade. This is useful
    for MA style strategies, whereas oscillator or diff style should be
    set to False (to often continue selling if above threshold, or
    buying below).
-   **TradeDelay:** How many candles with indicator info before allowing
    trades? *Must be equal to 1.*
-   **ReIssueSlippage:** What delta (as a percentage) of order price
    should we continue trying to get an order through for?
-   **ReIssueDelay:** How many seconds should we wait for an order to
    succeed before attempting to re-order? *This also affects the order
    delay*
-   **VolatilityThresholdOver:** Only available on volatility
    indicators. This is default enabled, and runs if the volatility
    indicator is above threshold. This may be set to *False* to revserse
    the behavior.

Simulator
---------

-   **Verbose**: Simulate trades using our paper trader. *Always
    simulates sells/buys at market bid/ask*
-   **Asset:** Number of BTC or LTC to start the simulation with.
-   **Currency:** Number of CNY or USD to start the simulation with.

Notifier
--------

-   **TextFile:** Record a log of all simulator and trader actions.
    -   **RolloverTime:** Time in hours to switch to a new log file.
    -   **BackupCount:** How many log files to keep? 0 to keep all.
    -   **Path:** Relative path to simulator and trader text file
        directory.
    -   **TradeName:** Filename for trader text file.
    -   **SimName:** Filename for simulator text file.
-   **Pushover:** Push notifications to your
    [Pushover](https://pushover.net/) account.
    -   **Simulator:** Enable for simulator actions.
    -   **Trader:** Enable for trader actions.
    -   **AppToken:** The Pushover *Application Token* to be used.
        Register a new app [here](https://pushover.net/apps/build)
    -   **UserKey:** Your Pushover *User Key* found on the Pushover
        dashboard.
-   **SMTP:** Non-TLS SMTP email support.
    -   **Simulator:** Enable for simulator actions.
    -   **Trader:** Enable for trader actions.
    -   **Host:** SMTP host to be used.
    -   **From:** SMTP account to send from.
    -   **To:** Email address to send to.
-   **TlsSMTP:** TLS SMTP email support. Configured for GMail by
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

-   **ShowTime:** Show time or show candle numbers as x axis labels?
-   **MaxLookback:** How many candles should we show on the graph
    (x-axis)?

Indicators
----------

-   Any **Trader** class nested inside an indicator class only effects
    the indicator if it's an independent indicator (not a combined
    indicator). See the "TradeIndicator" section above in documentation
    for more info.
-   All indicators are detailed in the [Indicators](indicators.md) page
    in documentation.
