# EIA Open Data API Python Client Package

This is an http client in python for the [U.S. Energy Information Administration (EIA) Open Data API](https://www.eia.gov/opendata/).

The API is vast and the quickest way to get an understanding for the endpoints is to use the [online browser](https://www.eia.gov/opendata/browser/).


## Installation

You can install the package from pypi. It is recommended to install it in a virtual environment.

``` bash

$ pip install eia-client

```

## Example

Below is a quick example showing how to submit a request to the
"total energy monthly" API endpoint for electricity net generation total
endpoint.

``` python

import eia_client as ec

endpoint = ec.endpoint.TotalEnergy(msn="ELETPUS")

client = ec.Client()
resp = client.get(endpoint.build())

df = ec.parse.as_dataframe(resp)
print(df.head())

df.to_csv("eia_data.csv")

```

You can view an extended version of this example and others in `examples/Quickstart_tminTutorial.ipynb`.

### Command line interface

There is a command line interface available at `eia_client.cli`. There are various commands that
can be run to assist in setting up the client (`config`) or downloading reports (`report`).

For example to run the config command do:

`python src/eia_client/cli.py config`

To run the report command:

`python src/eia_client/cli.py report`

There are other flags available for specifying output directories and file formats.

## API Key

Go to the [EIA Open Data API site](https://www.eia.gov/opendata/) and create, then downlaod an API key.

The package assumes the API Key for EIA is stored in your home directory as `~/.eia.config` (text) or an environment
variable called EIA_API_KEY.

*WARNING* Don't spam the API, there is nothing in the code to protect you from going over any rate limits; save the data and request as you need.


## Feature pipeline

- Endpoint query functionality to allow the user to discover endpoints.

- Walking endpoints without breaching rate limits.

- Backend adapters.

- Publish sphinx docs.

- Add more endpoints.

- Github workflow.

- CLI installation
