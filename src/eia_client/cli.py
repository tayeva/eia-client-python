"""Command line interface"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path
import logging

from eia_client import parse
from eia_client.client import Client
from eia_client import endpoint as ec_endpoint
import eia_client.api_key as ak


LOGGER = logging.getLogger(__name__)


def _clean_command(command: str) -> str:
    return command.lower()


def _config_command() -> ak.ApiKey:
    key = input("API Key:")
    ak.write(ak.get_default_config_file_path(), ak.ApiKey(key))


def _total_energy_monthly_report(client: Client, api_key: ak.ApiKey):
    msn = input("msn (default: ELETPUS; optional):")
    start = input("start (form: YYYY-MM; optional):")
    end = input("end (form: YYYY-MM; optional):")
    frequency = input("frequency (default: monthly; optional):")
    if not frequency:
        frequency = "monthly"
    if not msn:
        msn = "ELETPUS"
    endpoint = ec_endpoint.TotalEnergy(
        api_key=api_key, msn=msn, start=start, end=end, frequency=frequency
    )
    resp = client.get(endpoint.build())
    tem_df = parse.as_dataframe(resp)
    if not tem_df.empty:
        output_directory = input("output directory (default='.')")
        if not output_directory or output_directory.endswith("/"):
            output_directory = "."
        # TODO: add output format option
        output_file_path = Path(f"{output_directory}/total_energy_monthly.parquet")
        tem_df.to_parquet(output_file_path)
        LOGGER.info("Shape:%s", tem_df.shape)
        LOGGER.info("Wrote:%s", output_file_path)


def _electricity_retail_sales(client: Client, api_key: ak.ApiKey):
    # TODO: feature: add electricity reatail sales report
    pass


def _report_command(api_key: ak.ApiKey):
    report_to_run = input("Report (default: total_energy_monthly):")
    if not report_to_run:
        report_to_run = "total_energy_monthly"
    LOGGER.info("Running report:%s", report_to_run)
    client = Client()
    if report_to_run == "total_energy_monthly":
        _total_energy_monthly_report(client, api_key)
    elif report_to_run == "electricity-retail-sales":
        _electricity_retail_sales(client, api_key)


def _process_args(args: ArgumentParser):
    """Process the cli command."""
    command = _clean_command(args.command)
    if command == "config":
        _config_command()
    api_key = ak.load(config_file_path=args.api_key)
    if command == "report":
        _report_command(api_key)


def cli() -> ArgumentParser:
    """Command line interface."""
    arg_parser = ArgumentParser(
        prog="EIA Client",
        description="A friendly HTTP client for EIA.",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument(
        "command", choices=("config", "report"), help="Command to run."
    )
    arg_parser.add_argument(
        "-k", "--api-key", default=None, help="Optional API key file path."
    )
    _process_args(arg_parser.parse_args())


def main():
    """Main entry point for EIA client"""
    logging.basicConfig(level=logging.INFO)
    cli()


if __name__ == "__main__":
    main()
