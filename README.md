## Overview
This document will introduce you to a geocoding proxy service that accepts an address string and returns its latitude and longitude coordinates.

## How to Run the Service
#### Configuration

Please configure your host and port in `config.ini` under section `[BASE]`. By default these have been set to localhost:8000 for you.

#### Run the server
Start your server by calling:
```
python3 server.py
```
Once up, you may now access the service in a browser at the appropriate address as configured.

## How to use the Services API
This service has one GET request available that accepts the following query parameters

| Parameter | Type | Description |
| --- | --- | --- |
| address | str | A human readable address, for example: `1600 Pennsylvania Ave NW` |

It may be called directly in your browser.

Example:
- http://localhost:8000/?address=1600%20Pennsylvania%20Ave%20NW
