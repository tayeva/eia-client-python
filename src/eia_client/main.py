"""EIA client python main"""

import logging

from eia_client import cli


def main():
    """Main entry point for EIA client"""
    logging.basicConfig(level=logging.INFO)
    cli()


if __name__ == "__main__":
    main()
