# geocoding-proxy

# Overview
This document will introduce you to a geocoding proxy service that accepts an address string and returns its latitude and longitude coordinates.

# How to Run the Service
1. Please configure your host and port in `config.ini` under section `[BASE]`. By default these have been set to localhost:8000 for you.
2. Start your server by calling
```
python3 server.py
```
Once running, you may now access the service in a browser at the appropriate address as configured.

# How to use the Services API