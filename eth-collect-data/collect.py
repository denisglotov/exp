import argparse
import json
import os
import requests
import sys
import time


parser = argparse.ArgumentParser(
    description='Collect past transactions from ethereum network.')
parser.add_argument('--infura-api-token',
                    default=os.getenv('INFURA_API_TOKEN', default=''),
                    help='infura API token')
parser.add_argument('-n', '--network', default='mainnet',
                    help='network to query')
parser.add_argument('-v', '--verbose',  action='store_true',
                    help='print currently collected block')
parser.add_argument('--sleep', type=float, default=1,
                    help='delay between requests')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-s', '--start', type=int,
                   help='start with the specified block number')
group.add_argument('-m', '--minus', type=int,
                   help='start with latest block number minus this value')
args = parser.parse_args()


def ethRequest(method, *params):
    url = 'https://%s.infura.io/%s' % (args.network, args.infura_api_token)
    payload = {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}
    while True:
        try:
            ret = requests.post(url, data=json.dumps(payload))
        except requests.exceptions.SSLError:
            time.sleep(args.sleep)
        else:
            break
    ret.raise_for_status()
    return ret.json()['result']


def blockNumberToHex(blockNumber):
    return '0x%x' % blockNumber


if args.start:
    blockNumber = args.start
else:
    blockNumber = int(ethRequest('eth_blockNumber'), 16) - args.minus

while True:
    if args.verbose:
        sys.stderr.write('%d, ' % blockNumber)
    block = ethRequest('eth_getBlockByNumber',
                       blockNumberToHex(blockNumber),
                       False)
    if not block:
        break
    print '%s,' % json.dumps(block, indent=4)
    blockNumber += 1
    time.sleep(args.sleep)
