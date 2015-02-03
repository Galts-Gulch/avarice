Running
=======

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
-   Edit genconfig.py; find your own successful configuration. For full
    documentation, please check [here.](configuring.md)
-   Run python3 avarice.py - This software is meant to be run
    continuously, and will take awhile to generate valid info depending
    on configuration.
