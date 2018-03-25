Collect ethereum transactions
=============================

Use the following command to collect last 1000 blocks from rinkeby test
network to data.json file.

    python collect.py --network rinkeby --minus 1000 -v >>data.json

Process the data example:

    python process-hashes.py <data.json >data.csv
