#!/usr/bin/env python
# coding: utf-8
"""
CDD Vault Sample Deletion Script.

This script deletes all inventory Samples from a given vault in Collaborative 
Drug Discovery (CDD) via the REST API. It accepts a vault ID as a
command-line argument, sends a DELETE request using the configured API token,
and reports success or failure.

Usage example:
    python delete_all_samples.py -v VAULT_ID -t TOKEN
"""

import json
import argparse
import requests
from typing import Dict
from LOG_TOOL import set_logger


def argparser() -> argparse.Namespace:
    """Parse and return command-line arguments for file and vault IDs."""
    parser = argparse.ArgumentParser(description=
        """Given a CDD Vault ID Number.\nTHis script will delete all Samples
        within the Vault."""
    )

    parser.add_argument(
        "-v", "--vault_id",
        type=str, required=True,
        help="Vault ID number containing the file."
    )

    parser.add_argument(
        "-t", "--token",
        type=str, required=True,
        help="CDD API Token key string."
    )

    return parser.parse_args()


def get_sample_count(inv_url: str, header: Dict[str,str], logger) -> int:
    """
    Retrieves the count of inventory samples for a given vault ID using the
    provided API token.
    Args:
        vID (str): The vault ID.
        token (str): The API token for authentication.
    Returns:
        int: The count of inventory samples.
    """
    sampResponse: requests.Response
    sampResponse = requests.get(inv_url,
                                headers=header)

    if sampResponse.ok:
        sampDetails: Dict[str,str] = sampResponse.json()
        return sampDetails["count"]

    else:
        logger.warning(f"Failed to delete file:\n{sampResponse.text}")
        sampResponse.raise_for_status()


def delete_samples(vID: int, token: str, logger) -> None:
    """
    Deletes all inventory samples for a given vault ID using the provided API 
    token.

    Args:
        vID (int): The vault ID.
        token (str): The API token for authentication.

    Returns:
        None
    """
    sampResponse: requests.Response
    sampDetails: Dict[str,str]
    inv_samps: List[Dict[str,str]]

    root_url: str = f"https://app.collaborativedrug.com/api/v1/vaults"
    inv_url: str = f"{root_url}/{vID}/inventory_samples"
    header: Dict[str,str] = {"X-CDD-Token":token}
    count: int = get_sample_count(inv_url, header, logger)
    params: Dict[str,int] = {"page_size": count}
    
    if count <= 1000:
        sampResponse = requests.get(inv_url,
                                    headers=header,
                                    data=params)
        sampDetails = sampResponse.json()
        inv_samps = sampDetails["objects"]
    
        for i in inv_samps:
            s_resp: request.Response
            s_resp = requests.delete(f"inv_url/{i["id"]}",
                                     headers=header)

            if s_resp.ok:
                logger.info(f"DELETED SAMPLE ID {i["id"]}")

            else:
                logger.warning(f"Failed to delete sample:\n{s_resp.text}")
                response.raise_for_status()
    
    else:
        itr: int = int(count / 1000) + int(count % 0)
        offset: int = 1000

        while itr > 0:
            params: Dict[str,str] = {"offset": offset,
                                     "page_size": 1000}
            sampResponse = rt.get(inv_url,
                                  headers=header,
                                  data=params)

            if sampResponse.ok:
                sampDetails = sampResponse.json()
                inv_samps = sampDetails["objects"]
            
            else:
                logger.warning(f"Failed to get samples:\n{sampResponse.text}")
                response.raise_for_status()
            
            for i in inv_samps:
                s_resp2: reqeusts.Response
                sam_url: str = f"{inv_url}/{s['id']}"
                s_resp2 = rt.delete(sam_url,
                                    headers=header)

                if s_resp.ok:
                    logger.info(f"DELETED SAMPLE ID {i["id"]}")

                else:
                    logger.warning(f"Failed to delete sample: {s_resp.text}")
                    response.raise_for_status()
            
            offset += 1000
            itr -= 1

    return


def main():
    """Main f(x): parse arguments and delete CDD samples."""
    logger: logging.Logger
    args: argparse.Namespace

    logger = set_logger()
    logger.info(f"Program started.")
    args = argparser()
    delete_samples(args.vault_id, args.token, logger)
    logger.info(f"Program conplete.")

if __name__ == "__main__":
    main()
