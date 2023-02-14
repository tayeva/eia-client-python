"""Example total energy endpoint."""

import eia_client as ec


def main():
    """Example total energy endpoint."""
    endpoint = ec.endpoint.TotalEnergy()
    client = ec.Client()
    resp = client.get(endpoint.build())
    df = ec.parse.as_dataframe(resp)
    print(df.head())


if __name__ == "__main__":
    main()
