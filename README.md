# eia-client-python

This is an unofficial python package client package for the [U.S. Energy Information Administration (EIA) Open Data API](https://www.eia.gov/opendata/). It has minimal functionality and is under development. Please use it at your own risk.

The API is vast and the quickest way to get started is to use the [online browser](https://www.eia.gov/opendata/browser/) to select the API route you would like to query.

Mnemonic Series Names (MSN) - This is a unique identifier used by EIA for data series.

Example MSN:

Aviation Gasoline CO2 Emissions in Million Metric Tons of Carbon Dioxide (AVTCEUS)

The MSN is "AVTCEUS".

## Example


``` python

import eia_client as ec



```


## API Key

Go to the [EIA Open Data API site](https://www.eia.gov/opendata/) and create, then downlaod an API key.

The package assumes the API Key for EIA is stored in your home directory as `~/.eia.config` (text) or an environment
variable called EIA_API_KEY.

*Warning* Don't spam the API, there is nothing in the code to protect you from going over any rate limits; save the data and request as you need.
