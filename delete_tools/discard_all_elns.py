#!/usr/bin/env python
# coding: utf-8
"""
CDD Vault File Deletion Script.

This script deletes all ELN entries from a given vault in Collaborative Drug 
Discovery (CDD) via the REST API. It accepts the Vault ID as a 
command-line argument, sends a POST request to discard each entry using 
the given API token, and reports success or failure.

Usage example:
    python delete_all_elns.py -v VAULT_ID -t TOKEN
"""

import os
import re
import json
import requests
import argparse
from typing import List, Dict
from datetime import datetime
from LOG_TOOL import set_logger


def argparser() -> argparse.Namespace:
    """Parse and return command-line arguments for file and vault IDs."""
    parser = argparse.ArgumentParser(
        description=
        """Given a CDD Vault ID.\nThis script will delete all ELN entries."""
    )

    parser.add_argument(
        "--help_flag",
        help="CDD Vault API token."
    )

    parser.add_argument(
        "-v", "--vault_id",
        type=int, required=True,
        help="Vault ID number."
    )

    parser.add_argument(
        "-t", "--token",
        type=str, required=True,
        help="CDD API Token key string."
    )
    
    return parser.parse_args()


def get_eln_ids(vID: int, token: str) -> Dict[str,str]:
    """
    Send a GET request to the CDD API to retrieve ELN details.
    
    Args:
        vID (int): ID of the Vault with ELNs.
        token (str): CDD API key.
    
    Return:
        eln_id_list (list): List of CDD Vault ELN ID numbers.
    
    Raises:
        HTTPError: If the request fails (non-2xx status code).
    """
    eln_response: requests.response

    root_url: str = f"https://app.collaborativedrug.com/api/v1/vaults/"
    eln_url: str = f"{root_url}{vID}/eln/entries"
    header: Dict[str,str] = {"X-CDD-Token":token}
    params: Dict[str,str] = {"only_ids":True}

    eln_response = requests.get(eln_url,
                                headers=header,
                                data=params)
    
    if eln_response.ok:
        eln_details: Dict[str,str] = eln_response.json()
        eln_id_list: List[int] = eln_details["objects"]
        logger.info(f"{len(eln_id_list)} ELNs found")
        return eln_id_list
    
    else:
        logger.warning(f"Failed to get ELNs: {response.text}")
        response.raise_for_status()
    
    

def discard(vID: int, token: str, eln_id_list: List[int]) -> None:
    """
    Send a DELETE request to the CDD API to remove a file from a vault.
    
    Args:
        vID (str): ID of the file to delete.
        token (str): ID of the vault containing the file.
        eln_id_list (list): List of CDD Vault ELN ID numbers.
    
    Raises:
        HTTPError: If the request fails (non-2xx status code).
    """
    update_resp: requests.Response

    root_url: str = f"https://app.collaborativedrug.com/api/v1/vaults/"
    eln_url: str = f"{root_url}{vID}/eln/entries"
    header: Dict[str,str] = {"X-CDD-Token":token}
    params: Dict[str,str] = {"status_action":"discard"}

    for e in eln_id_list:
        update_resp = requests.post(f"{eln_url}/{e}/status",
                                    headers=header,
                                    data=params)

        if not update_resp.ok:
            logger.warning(f"Failed to update ELN: {update_resp.text}")
            update_resp.raise_for_status()
        else:
            logger.info(f"ELN ID # {e} DISCARDED")
        

def main():
    """Main f(x): parse arguments and discade ELN entries."""
    args: argparse.Namespace

    args = argparser()
    if args.help_flag:
        parser.print_help()
        sys.exit(0)

    logger: logging.Logger
    logger = set_logger()
    logger.info("Program started.")

    eln_ids: List[int] = get_eln_ids(args.vault_id,
                                     args.token,
                                     logger)
    
    discard(args.vault_id,
            args.token,
            eln_ids,
            logger)
    
    logger.info("Program completed.")

if __name__ == "__main__":
    main()
  

