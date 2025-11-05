#!/usr/bin/env python
# coding: utf-8
"""
CDD Vault File Deletion Script.

This script deletes a specified file from a given vault in Collaborative Drug 
Discovery (CDD) via the REST API. It accepts the file ID and vault ID as 
command-line arguments, sends a DELETE request using the given API token,
and reports success or failure.

Usage example:
    python delete_file_by_id.py -f FILE_ID -v VAULT_ID -t TOKEN
"""

import argparse
import requests
from typing import Dict
from LOG_TOOL import set_logger


def parse_arguments() -> argparse.Namespace:
    """Parse and return command-line arguments for file and vault IDs."""
    parser = argparse.ArgumentParser(
        description=
        """Given a CDD Vault File ID # and a CDD Vault ID #.\n
        This script will delete the file."""
    )

    parser.add_argument(
        "--help_flag",
        help="CDD Vault API token."
    )

    parser.add_argument(
        "-f", "--file_id",
        type=int, required=True,
        help="File ID number to delete."
    )

    parser.add_argument(
        "-v", "--vault_id",
        type=int, required=True,
        help="Vault ID number containing the file."
    )

    parser.add_argument(
        "-t", "--token",
        type=str, required=True,
        help="CDD API Token key string."
    )

    return parser.parse_args()


def delete_file(file_id: int, vault_id: int, api_token: str, logger) -> None:
    """
    Send a DELETE request to the CDD API to remove a file from a vault.

    Args:
        file_id (int): ID of the file to delete.
        vault_id (int): ID of the vault containing the file.
        api_token (str): CDD Vault API Token string.
    
    Raises:
        HTTPError: If the request fails (non-2xx status code).
    """
    response: reqeusts.Response

    root_url: str = f"https://app.collaborativedrug.com/api/v1/vaults"
    file_url: str = f"{root_url}/{vault_id}/files/{file_id}"
    header: Dict[str,str] = {"X-CDD-Token":api_token}
    
    response = requests.delete(file_url,
                               headers=header,
                               timeout=5.0)
    
    if response.ok:
        logger.info(f"DELETED FILE ID {file_id}")
        return
    
    else:
        logger.warning(f"Failed to delete file: {response.text}")
        response.raise_for_status()


def main() -> None:
    """Main f(x): parse arguments and delete the specified file."""
    args: argparse.Namespace

    args = parse_arguments()
    if args.help_flag:
        parser.print_help()
        sys.exit(0)

    logger: logging.Logger
    logger = set_logger()
    logger.info(f"Program started.")
    
    delete_file(args.f, args.v, args.t, logger)
    logger.info(f"Program conplete.")


if __name__ == "__main__":
    main()
