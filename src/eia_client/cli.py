"""Command line interface"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path
import logging

from eia_client.api_endpoint import ApiEndpointBuilder
from eia_client.api_key import (ApiKey, write_api_key, load_api_key,
                                get_default_config_file_path)
from eia_client import client


LOGGER = logging.getLogger(__name__)


def _clean_command(command : str) -> str:
    return command.lower()


def _config_command() -> ApiKey:
    api_key = input("API Key:")
    write_api_key(get_default_config_file_path(), ApiKey(api_key))


def _report_command(api_key: ApiKey):
    report_to_run = input("Report (default: total_energy_monthly):")
    if not report_to_run:
        report_to_run = "total_energy_monthly"
    LOGGER.info("Running report:%s", report_to_run)
    api_endpoint_builder = ApiEndpointBuilder(api_key)
    if report_to_run == "total_energy_monthly":
        msn = input("msn (default: ELETPUS):")
        if not msn:
            msn = "ELETPUS"
        resp = client.get(api_endpoint_builder.total_energy_monthly(msn))
        tem_df = client.parse_as_dataframe(resp)
        if not tem_df.empty:
            output_directory = input("output directory (default='.')")
            if not output_directory or output_directory.endswith("/"):
                output_directory = "."
            output_file_path = Path(f"{output_directory}/total_energy_monthly.parquet")
            tem_df.to_parquet(output_file_path)
            LOGGER.info("Shape:%s", tem_df.shape)
            LOGGER.info("Wrote:%s", output_file_path)


def _process_args(args : ArgumentParser):
    """Process the cli command."""
    command = _clean_command(args.command)
    if command == "config":
        _config_command()
    api_key = load_api_key(config_file_path=args.api_key)
    if command == "report":
        _report_command(api_key)


def cli() -> ArgumentParser:
    """Command line interface."""
    arg_parser = ArgumentParser(prog="EIA Client", description="A friendly HTTP client for EIA.",
                                formatter_class=ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument("command", choices=("config", "report"), help="Command to run.")
    arg_parser.add_argument("-k", "--api-key", default=None, help="Optional API key file path.")
    _process_args(arg_parser.parse_args())
