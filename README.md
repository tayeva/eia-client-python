# EIA Open Data API Python Client Package

This is an unofficial http client in python for the [U.S. Energy Information Administration (EIA) Open Data API](https://www.eia.gov/opendata/). It has minimal functionality and is under development. Please use it at your own risk.

The API is vast and the quickest way to get started is to use the [online browser](https://www.eia.gov/opendata/browser/) to select the API route you would like to query.

Mnemonic Series Names (MSN) - This is a unique identifier used by EIA for data series.

Example MSN:

Electricity Net Generation Total

The MSN is "ELETPUS".

## Installation

You can install the package from pypi. It is recommended to install in a virtual environment.

``` bash

$ pip install eia-client

```

## Example

Below is a quick example showing how to submit a request to the
"total energy monthly" API endpoint for electricity net generation total
endpoint.

``` python

import eia_client as ec

# Under the hood this reads your API key and builds it into the requests.
builder = ec.EndpointBuilder()
endpoint = builder.total_energy(msn="ELETPUS")

client = ec.Client()
resp = client.get(endpoint)

df = ec.parse.as_dataframe(resp)
print(df.head())

df.to_csv("eia_data.csv")

```

You can view an extended version of this example in `examples/Quickstart_tminTutorial.ipynb`.


## API Key

Go to the [EIA Open Data API site](https://www.eia.gov/opendata/) and create, then downlaod an API key.

The package assumes the API Key for EIA is stored in your home directory as `~/.eia.config` (text) or an environment
variable called EIA_API_KEY.

*WARNING* Don't spam the API, there is nothing in the code to protect you from going over any rate limits; save the data and request as you need.


## Feature pipeline

- Endpoint query functionality to allow the user to discover endpoints.

- Walking endpoints without breaching rate limits.

- Backend adapters.
