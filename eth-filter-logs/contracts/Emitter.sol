// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;


contract Emitter {
    event A(uint256 indexed a);
    event B(uint256 indexed b1, uint256 b2);
    event C(uint256 indexed c1, string c2);
    event D(uint256 indexed d1, uint8 indexed d2, string d3);

    function send() public {
        emit A(1);
        emit B(2, 22);
        emit B(3, 33);
        emit C(4, "44");
        emit D(5, 55, "555");
    }
}
