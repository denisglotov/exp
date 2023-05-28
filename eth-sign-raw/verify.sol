// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;

contract Ecrecover {
        function show(uint8 v, bytes32 r, bytes32 s, bytes32 border, bytes32 salt) external pure returns (address, bytes32, bytes memory) {
            bytes memory data = abi.encode(uint8(0x02), border, salt);
            bytes32 hash = keccak256(data);
            return (ecrecover(hash, v, r, s), hash, data);
        }
}
