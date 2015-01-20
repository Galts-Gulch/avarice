avarice
=======

*(noun) extreme greed for wealth or material gain.*

*Greed captures the essence of the evolutionary spirit.* -Gordon Gekko

INDEX
-----

-   [Disclaimer](https://github.com/Galts-Gulch/avarice#disclaimer)
-   [Notes](https://github.com/Galts-Gulch/avarice#notes)
-   [Contributing](https://github.com/Galts-Gulch/avarice#contributing)
-   [Feature Highlight](https://github.com/Galts-Gulch/avarice#feature-highlight)
-   [Supported Indicators](https://github.com/Galts-Gulch/avarice#supported-indicators)
-   [Running](https://github.com/Galts-Gulch/avarice#running)
-   [Donations](https://github.com/Galts-Gulch/avarice#donations)

Disclaimer
----------

-   Please understand what you are doing before attempting to live trade
    at all. Any money you may lose is your own responsibility.
-   Please see LICENSE.txt for license info

Notes
-----

-   This software is expected to run continuously to get valid data. We
    do however support resuming if the downtime is less than the
    configured CandleSize.
-   All testing is done on current Python3.5.

Contributing
------------

-   Check
    [docs/Contributing.md](https://github.com/Galts-Gulch/avarice/blob/master/docs/Contributing.md)
    for details on adding an exchange, or other contributions.

Feature Highlight
-----------------

-   Can utilize a list of multiple indicators to trade off for more
    secure trade decisions.
-   Separate WebSocket API connections for private and public
    interactions.
-   Can easily customize the indicators used.
-   Many indicators support multiple trade strategies.
-   Simulation mode allows simulating trades without live trading, or
    requiring an exchange account.
-   Live trading mode at market prices.
-   Interactive graphs may be created in real time for selected trade
    indicators and price. *Mouseover Examples:
    [price](http://imgh.us/price_chart.svg),
    [KDJ](http://imgh.us/KDJ_chart.svg),
    [MACD](http://imgh.us/MACD_chart.svg)*
-   Consistently pursuing a cleaner base to allow easier community
    involvement.

Supported Indicators
====================

SMA (Simple Movement Average)
-----------------------------

-   NOTE: We support two SMA trade strategies specified in
    genconfig.SMA.IndicatorStrategy; "CD" (convergence/divergence), and
    "Diff" (waits to pass up or down diff threshold before trend is
    determined)
-   Does two calculations off SMAShortPeriod and SMALongPeriod
-   SMA = (Sum of last SMAPeriod candles) / SMAPeriod
-   SMADiff = 100 \* (shortSMA - longSMA) / ((shortSMA + longSMA) / 2)

EMA (Exponential Movement Average)
----------------------------------

-   NOTE: We support two EMA trade strategies specified in
    genconfig.EMA.IndicatorStrategy; "CD" (convergence/divergence), and
    "Diff" (waits to pass up or down diff threshold before trend is
    determined
-   We trade this as a crossover (convergence/divergence) indicator.
    This is one of our supported EMA trade strategies. On 10/21, when
    EMA10 \< EMA21, we sell (and visa versa). Differs from MACD due to
    lack of third signal line.
-   NOTE: does two calculations using EMAShort and EMALong.
-   The first iteration uses SMA to generate the first EMA.
-   Multiplier = (2 / EMAPeriod) + 1
-   EMA = ((Current Close - Previous EMA) \* Multiplier) + Previous EMA
-   EMADiff = 100 \* (shortEMA - longEMA) / ((shortEMA + longEMA) / 2)

EMAwbic (Exponential Movement Average using @wbic16 logic)
----------------------------------------------------------

-   NOTE: it's recommended to set genconfig's SingleTrade to False, and
    lower TradeVolume if acting as the only indicator. When used with
    other indicators, it aids in mean reversion confirmation.
-   This buys when the price is \< Bid Percent of the EMA, and sells
    when the price is \> Ask Percent of the EMA.

DEMA (Double Exponential Movement Average)
------------------------------------------

-   NOTE: We support two DEMA trade strategies specified in
    genconfig.DEMA.IndicatorStrategy; "CD" (convergence/divergence), and
    "Diff" (waits to pass up or down diff threshold before trend is
    determined
-   Similar points as the "EMA" section above, however with more of a
    weight on the last EMA (LOWER LATENCY THAN EMA).
-   DEMA = 2 \* EMA – EMA(EMA)
-   DEMADiff = 100 \* (shortDEMA - longDEMA) / ((shortDEMA + longDEMA) /
    2)  

FRAMA (Fractal Adaptive Moving Average)
---------------------------------------

-   NOTE: We support two FRAMA trade strategies specified in
    genconfig.FRAMA.IndicatorStrategy; "CD" (convergence/divergence),
    and "Diff" (waits to pass up or down diff threshold before trend is
    determined
-   N = (highest price - lowest price) / period ; split into 3 periods -
    first half, second half, full period.
-   D = (Log(N1 + N2) - Log(N3)) / Log(2)
-   Alpha = exp(-4.6 \* (D-1))
-   FRAMA = Alpha \* Price + (1 - Alpha) \* LastFRAMA
-   FRAMADiff = 100 \* (shortFRAMA - longFRAMA) / ((shortFRAMA +
    longFRAMA) / 2)

MACD (Moving Average Convergence-Divergence)
--------------------------------------------

-   NOTE: We support two MACD trade strategies specified in
    genconfig.MACD.IndicatorStrategy; "CD" (convergence/divergence), and
    "Diff".
-   CD: When MACD \< signal, we sell (and visa versa).
-   Diff: Traditionally, this MACD strategy would sell if MACD goes
    below zero line (and visa versa). We do the same, but for MACDDiffUp
    and MACDDiffDown for fewer false positives (recommend configuring as
    you see fit).
-   MACD = MACDShortEMA - MACDLongEMA
-   MACDSignal = MACDSignal period EMA of MACD

DMACD (Double Moving Average Convergence-Divergence)
----------------------------------------------------

-   We use MACDLong, MACDShort, and MACDPeriod settings for DMACD
-   NOTE: We support two DMACD trade strategies specified in
    genconfig.DMACD.IndicatorStrategy; "CD" (convergence/divergence),
    and "Diff".
-   Similar to the MACD section above, except we use DEMAs instead of
    EMAs (yes, even on signal). See DEMA above if unsure what this
    means.

RSI (Relative Strength Index Oscillator)
----------------------------------------

-   NOTE: avg gains and losses are smoothed after first iteration
-   NOTE: Want to try out RSI(2) or RSI(3)? Set those periods (2 or 3),
    and run 90/10 or 95/5 as ask/bid thresholds.
-   RS = avg\_gain / avg\_loss
-   RSI = 100 - (100 / (1 + RSI))

FastStochRSI (Stochastic RSI Oscillator)
----------------------------------------

-   NOTE: lowest/highest are from RSIPeriod
-   FastStochRSIK = ((RSI - Lowest RSI) / (Highest RSI - Lowest RSI)) \*
    100
-   FastStochRSID = FastStochRSIDPeriod SMA of FastStochRSIK

FullStochRSID
-------------

-   FullStochasticRSID = FullStochRSIDPeriod SMA of FastStochRSID

FastStochK (Fast Stochastic Oscillator %K)
------------------------------------------

-   FastStochasticK = ((Current Close - Low) / (High - Low)) \* 100

FastStochD
----------

-   FastStochasticD = FastStochDPeriod SMA of %K

FullStochD
----------

-   NOTE: FullStochK is not includes since it's equivalent to FastStochD
-   FullStochasticD = FullStochDPeriod SMA of Fast %D

KDJ
---

-   NOTE: Uses *new* FullStoch %K and FullStoch %D calculations.
-   NOTE: Supports both CD and Diff in genconfig.KDJ.IndicatorStrategy.
-   CD: When K \< D, we sell (and visa versa)
-   Diff: When J is above KDJJAsk, we sell. When J is below KDJJBid, we
    buy. J may go above and below 100 and 0.
-   J = (3 \* D) - (2 \* K)

Aroon (Aroon Oscillator)
------------------------

-   NOTE: Supports both CD and Diff in
    genconfig.Aroon.IndicatorStrategy.
-   CD: When AroonOscillator \< 0, we sell (and visa versa). This is
    because when AroonOscillator is 0, AroonUp and AroonDown
    converge/diverge.
-   Diff: When Aroon is below AroonBid, we buy. When Aroon is above
    AroonAsk, we sell.
-   AroonUp = 100 \* ((AroonPeriod - Candles since last AroonPeriod
    high) / AroonPeriod)
-   AroonDown = 100 \* ((AroonPeriod - Candles since last AroonPeriod
    low) / AroonPeriod)
-   Aroon = AroonUp - AroonDown

Ichimoku (Ichimoku Cloud)
-------------------------

-   NOTE: Utilizes Ichimoku.IndicatorStrategy for "Strong" or "Weak"
    strategies.
-   NOTE: Chikou Span's cool and all, but we don't care. We want to
    trade in real time, and a price list 26 periods behind only confirms
    if we *were* right or wrong. Because proper Ichimoku cloud relies on
    Senkou Span A being plotted ChikouSpan periods in the future, we
    still set this integer.
-   Strong: if (price \> Ichimoku cloud min) and (price \< Kijun-Sen)
    and (price \> Tenkan-Sen), sell. Buy on the inverse.
-   Weak: if (Tenkan-Sen \> Kijun-Sen), sell. Buy on the inverse. Weak
    is more of a standard C-D strategy.
-   Tenkan-sen = (TenkanSenPeriod high + TenkanSenPeriod low)/2))
-   Kijun-sen = (KijunSenPeriod high + KijunSenPeriod low)/2))
-   Senkou Span A = (Tenkan-sen + Kijun-sen)/2)) ; Plotted
    ChikouSpanPeriods in the future.
-   Senkou Span B = (SenkouSpanPeriod high + SenkouSpanPeriod low)/2))

StdDev (Sampled Standard Deviation)
-----------------------------------

-   NOTE: Only here to be used by other volatility indexes
-   The following is ripped/edited from stockcharts.com since it
    summarizes the Std Dev calculations quite well:
    -   Calculate the average (mean) price for the number of periods or
        observations.
    -   Determine each period's deviation (close less average price).
    -   Square each period's deviation.
    -   Sum the squared deviations.
    -   Divide this sum by the number of samples.
    -   The standard deviation is then equal to the square root of that
        number.

BollBands (Bollinger Bands)
---------------------------

-   Middle Band = BollBandPeriod SMA
-   Upper Band = BollBandPeriod SMA + (BollBandPeriod StdDev \* 2)
-   Lower Band = BollBandPeriod SMA - (BollBandPeriod StdDev \* 2)

SROC (Simple Rate of Change AKA Movement)
-----------------------------------------

-   SROC = (Close - Close n periods ago)
-   if current SROC \> 0, and previous SROC \<= 0, BUY. Sell during the
    inverse.

Running
-------

-   Python 3.4 or higher
-   Dependencies (can be easily installed using pip3)
    -   websockets for OKCoin API
    -   websocket-client for trading on OKCoin API (maintains a separate
        connection from public websockets API)
    -   pygal for graphing (not required as long as genconfig.Grapher is
        disabled)
    -   lxml for pygal (not required as long as genconfig.Grapher is
        disabled)
-   Clone or grab a release from the
    [releases](https://github.com/Galts-Gulch/avarice/releases) page.
-   Edit genconfig.py; find your own successful configuration.
-   Run python3 avarice.py - This software is meant to be run
    continuously, and will take awhile to generate valid info depending
    on configuration.

Donations
---------

Donations are not at all required, or even really requested. If you want
to show a "thank you," and can't contribute code, then feel free to
donate. BTC: 18XCHsFFpnSWv2GZTbQbXtGTSQGrZABueZ
