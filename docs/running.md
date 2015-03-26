Running
=======

-   Python 3.4 or higher
-   Dependencies:
    - To install all dependencies using pip3:

            pip3 install -r requirements.txt

    -   websockets for OKCoin API
        -   Using pip3:

                pip3 install websockets

    -   websocket-client for trading on OKCoin API (maintains a separate
        connection from public websockets API)
        -   Using pip3:

                pip3 install websocket-client

    -   pygal for graphing (Only needed if graphing is desired)
        -   Using pip3:

                pip3 install pygal

    -   lxml for pygal (Only needed if graphing is desired)
        -   Using pip3:

                pip3 install lxml

-   Clone development version or grab a release from the
    [releases](https://github.com/Galts-Gulch/avarice/releases) page.
-   Edit genconfig.py; find your own successful configuration. For full
    documentation, please check [here.](configuring.md)
-   Run python3 avarice.py - This software is meant to be run
    continuously, and will take awhile to generate valid info depending
    on configuration.
