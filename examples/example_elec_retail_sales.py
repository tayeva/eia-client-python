"""Example electricity retail sales."""

import eia_client as ec


def main():
    """Example electricity retail sales."""
    endpoint = ec.endpoint.ElectricityRetailSales(
        data="price", state=["CA", "NY"], sector="RES"
    )
    client = ec.Client()
    resp = client.get(endpoint.build())
    df = ec.parse.as_dataframe(resp)
    print(df.head())


if __name__ == "__main__":
    main()
