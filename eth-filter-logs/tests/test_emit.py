#!/usr/bin/python3

from web3 import datastructures, exceptions
import pytest
import json


@pytest.fixture
def emitter(Emitter, accounts):
    return Emitter.deploy({'from': accounts[0]})


def test_emit(accounts, emitter, web3, Emitter):
    # Invoke send() method of Emitter contract instance
    tx = emitter.send({'from': accounts[0]})
    assert len(tx.events) == 5

    # Prepare filter for 3 events (out of 4 emitted)
    filt = web3.eth.filter(
        {
            'address': emitter.address,
            'fromBlock': tx.block_number,
            'toBlock': tx.block_number,
            'topics': [[
                web3.keccak(text="Alfa(uint256)").hex(),
                web3.keccak(text="Bravo(uint256,uint256)").hex(),
                web3.keccak(text="Delta(uint256,uint8,string)").hex(),
            ]]
        }
    )

    # Query the desiered logs
    logs = web3.eth.get_filter_logs(filt.filter_id)

    # Parse them using web3 log parsers
    # This O(n^2) approach is not optimal, I didn't find a simple way to
    # locate contract.event by its topic[0]. Although it would be faster
    contract = web3.eth.contract(abi=Emitter.abi)
    parsed_logs = []
    for event in logs:
        for evt in contract.events:
            try:
                parsed_logs.append(evt().processLog(event))
                break
            except exceptions.MismatchedABI:
                pass

    # Pretty print the result
    with open("out.txt", "w") as out:
        out.write(json.dumps(parsed_logs, cls=JsonEthereumEncoder, indent=4))


class JsonEthereumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.hex()
        elif isinstance(obj, datastructures.AttributeDict):
            return dict(obj)
        return json.JSONEncoder.default(self, obj)
