#!/usr/bin/env python3
"""
Usage: virustotal-filecheck.py ARG_FILE

Let's call it a convenience script, that wraps the VirusTotal "get-file-report"
functionality for the purpose of conveniently sending a file inquiry from the
command line.

Please provide your own API key for VirusTotal and store it in an environment
variable called "VT_API_KEY".
"""


import os
import sys
import hashlib
import requests


VT_API_URL = 'https://www.virustotal.com/vtapi/v2/file/report'
VT_API_ENVVAR_NAME = 'VT_API_KEY'


# -----------------------------------------------------------------------------

def get_file_hash(file_path: str) -> str:
    """
    Pick up the file specified, read it, compute SHA256 hash.
    :param file_path: where to read the file from
    :raises FileNotFoundError: when the input file is missing
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


def print_response(rj: dict) -> None:
    """
    Print the response, but somewhat refine it first.
    We don't need all of the details prited.
    :param rj: the response dictionary
    """
    print('---------')
    if 'permalink' not in rj:
        print(f"verbose_msg : {rj['verbose_msg']}")
    else:
        print(f"permalink : {rj['permalink']}")
        print(f"scan_date : {rj['scan_date']}")
        print(f"positives : {rj['positives']} (/{rj['total']})")
        for scanres in rj['scans']:
            if rj['scans'][scanres]['detected']:
                print(f"  {scanres} -> {rj['scans'][scanres]['result']}")


# -----------------------------------------------------------------------------

if __name__ == '__main__':

    API_KEY = os.getenv(VT_API_ENVVAR_NAME)
    if not API_KEY:
        print(f' *** Environment variable {VT_API_ENVVAR_NAME} not found',
              file=sys.stderr)
        sys.exit(2)

    if len(sys.argv) == 2:
        FILE_PATH = sys.argv[1]
    else:
        print(' *** please name a file for VT to check :)', file=sys.stderr)
        print(file=sys.stderr)
        sys.exit(1)

    #
    FISHA256 = get_file_hash(FILE_PATH)

    print()
    print(f'File   :  {FILE_PATH}')
    print(f'sha256 :  {FISHA256}')

    params = {'apikey': API_KEY, 'resource': FISHA256}
    response = requests.get(VT_API_URL, params=params)

    if response.ok:
        print_response(response.json())
        print()
    else:
        print(f' *** [{response.status_code}] -> {response.text}',
              file=sys.stderr)
