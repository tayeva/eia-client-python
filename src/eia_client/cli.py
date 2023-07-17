"""Command line interface"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Namespace
from pathlib import Path
import logging

import pandas as pd

from eia_client import parse
from eia_client.client import Client
from eia_client import endpoint as ec_endpoint
import eia_client.api_key as ak


LOGGER = logging.getLogger(__name__)


def _clean_command(command: str) -> str:
    return command.lower()


def _config_command() -> None:
    try:
        key = input("API Key:")
    except KeyboardInterrupt:
        return None
    ak.write(ak.get_default_config_file_path(), ak.ApiKey(key))


def _dataframe_writer(df: pd.DataFrame, args: Namespace, report_name: str) -> None:
    if df.empty:
        LOGGER.warning("Dataframe is empty. No data to write.")
        return None
    if args.output_directory is None:
        output_directory = input("output directory (default='./')")
        if not output_directory:
            output_directory = "./"
    else:
        output_directory = args.output_directory
    output_directory = Path(output_directory)
    if not output_directory.exists():
        LOGGER.info("Created directory:%s", output_directory)
        output_directory.mkdir(parents=True)
    if args.output_format == "parquet":
        file_ext = ".parquet"
    else:
        file_ext = ".csv"
    output_file_path = output_directory.joinpath(f"{report_name}{file_ext}")
    if file_ext == ".parquet":
        df.to_parquet(output_file_path)
    else:
        df.to_csv(output_file_path)
    LOGGER.info("Shape:%s", df.shape)
    LOGGER.info("Wrote:%s", output_file_path)


def _total_energy_monthly_report(client: Client, api_key: ak.ApiKey, args: Namespace):
    msn = input("msn (default: ELETPUS; optional):")
    start = input("start (form: YYYY-MM; optional):")
    end = input("end (form: YYYY-MM; optional):")
    frequency = input("frequency (default: monthly; optional):")
    if not start:
        start = None
    if not end:
        end = None
    if not frequency:
        frequency = "monthly"
    if not msn:
        msn = "ELETPUS"
    endpoint = ec_endpoint.TotalEnergy(
        api_key=api_key, msn=msn, start=start, end=end, frequency=frequency
    )
    resp = client.get(endpoint.build())
    tem_df = parse.as_dataframe(resp)
    _dataframe_writer(tem_df, args, report_name="total_energy_monthly")


def _electricity_retail_sales(client: Client, api_key: ak.ApiKey):
    # TODO: feature: add electricity reatail sales report
    LOGGER.warning("Electricity sales not yet implemented.")


def _report_command(api_key: ak.ApiKey, args: Namespace):
    report_to_run = input("Report (default: total_energy_monthly):")
    if not report_to_run:
        report_to_run = "total_energy_monthly"
    LOGGER.info("Running report:%s", report_to_run)
    client = Client()
    if report_to_run == "total_energy_monthly":
        _total_energy_monthly_report(client, api_key, args)
    elif report_to_run == "electricity-retail-sales":
        _electricity_retail_sales(client, api_key)


def _process_args(args: ArgumentParser):
    """Process the cli command."""
    command = _clean_command(args.command)
    if command == "config":
        _config_command()
    api_key = ak.load(config_file_path=args.api_key)
    if command == "report":
        _report_command(api_key, args)


def cli() -> None:
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
    arg_parser.add_argument(
        "--output-format",
        choices=("csv", "parquet"),
        default="parquet",
        help="Output format.",
    )
    arg_parser.add_argument(
        "--output-directory", default=None, help="Output directory."
    )
    _process_args(arg_parser.parse_args())


def main():
    """Main entry point for EIA client"""
    logging.basicConfig(level=logging.INFO)
    cli()


if __name__ == "__main__":
    main()
