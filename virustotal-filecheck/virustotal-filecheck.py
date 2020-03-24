#!/usr/bin/env python3
"""
Usage: virustotal-filecheck.py ARG_FILE

Let's call it a convenient script, that wraps the VirusTotal get-file-report functionality
for the purpose of conveniently sending a file inquiry from the command line.
Please provide your own API key for VT and put it into a file called "auth.py",
as a string named "APIKEY".
"""


import sys
import hashlib
import requests

try:
    from auth import APIKEY
except ImportError as e:
    print(f' *** {e}', file=sys.stderr)
    print(' *** Put your VirusTotal "APIKEY" string in a file named "auth.py" here.', file=sys.stderr)
    sys.exit(2)


VTAPIURL = 'https://www.virustotal.com/vtapi/v2/file/report'


def get_file_hash(filename):  # raises FileNotFoundError
    sha256_hash = hashlib.sha256()
    with open(filename, 'rb') as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


def print_response(rj):
    """
    Somewhat refine the response.
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


if __name__ == '__main__':

    if len(sys.argv) == 2:
        FILENAME = sys.argv[1]
    else:
        print(' *** please name a file for VT to check :)', file=sys.stderr)
        sys.exit(1)

    FISHA256 = get_file_hash(FILENAME)

    print(f'File   :  {FILENAME}')
    print(f'sha256 :  {FISHA256}')

    params = {'apikey': APIKEY, 'resource': FISHA256}
    response = requests.get(VTAPIURL, params=params)

    if response.ok:
        print_response(response.json())
    else:
        print(f' *** [{response.status_code}] -> {response.text}', file=sys.stderr)
