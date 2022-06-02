#!/usr/bin/python3

from web3 import datastructures, exceptions
import pytest
import json


@pytest.fixture
def emitter(Emitter, accounts):
    return Emitter.deploy({'from': accounts[0]})


def test_emit(accounts, emitter, web3, Emitter):
    tx = emitter.send({'from': accounts[0]})

    assert len(tx.events) == 5
    filt = web3.eth.filter(
        {
            'address': emitter.address,
            'fromBlock': tx.block_number,
            'toBlock': tx.block_number,
            'topics': [[
                web3.keccak(text="A(uint256)").hex(),
                web3.keccak(text="B(uint256,uint256)").hex(),
                web3.keccak(text="D(uint256,uint8,string)").hex(),
            ]]
        }
    )
    logs = web3.eth.get_filter_logs(filt.filter_id)

    contract = web3.eth.contract(abi=Emitter.abi)
    parsed_logs = []
    for event in logs:
        for evt in contract.events:
            try:
                parsed_logs.append(evt().processLog(event))
                break
            except exceptions.MismatchedABI:
                pass

    with open("out.txt", "w") as out:
        out.write(json.dumps(parsed_logs, cls=JsonEthereumEncoder, indent=4))


class JsonEthereumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.hex()
        elif isinstance(obj, datastructures.AttributeDict):
            return dict(obj)
        return json.JSONEncoder.default(self, obj)
