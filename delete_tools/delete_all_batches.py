import json
import argparse
import requests as rt


def argparser():
    parser = argparse.ArgumentParser(
        description=
        """Given a CDD Vault ID.\nThis script will delete all Batches."""
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


def get_batch_ids(vID, apiToken):
    root_url = "https://app.collaborativedrug.com/api/v1/vaults"
    response = rt.get(f"{root_url}/{vID}/batches",
                      headers={"X-CDD-Token": apiToken},
                      data={"only_ids": "true"})
    try:
        if response.status_code == 200:
            resp_dets = response.json()
            return resp_dets["objects"]
    except ValueError:
        raise Exception(response.text)


def delete_batch(vID, apiToken, batch_id):
    root_url = "https://app.collaborativedrug.com/api/v1/vaults"
    batch_url = f"{root_url}/{vID}/batches/{batch_id}"
    header = {"X-CDD-Token": apiToken, "Content-Type": "application/json"}
    parameters = json.dumps({"projects": []})
    batch_response = rt.put(batch_url, headers=header, data=parameters)
    batch_dets = batch_response.json()
    return


def main():
    """Main f(x): parse arguments and delete CDD samples."""
    args = argparser()
    batch_ids = get_batch_ids(args.vault_id, args.token)
    for bID in batch_ids:
        delete_batch(args.vault_id, args.token, bID)
      

if __name__ == "__main__":
    main()
