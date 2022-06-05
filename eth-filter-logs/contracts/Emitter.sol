// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;


contract Emitter {
    event Alfa(uint256 indexed a);
    event Bravo(uint256 indexed b1, uint256 b2);
    event Charlie(uint256 indexed c1, string c2);
    event Delta(uint256 indexed d1, uint8 indexed d2, string d3);

    function send() public {
        emit Alfa(1);
        emit Bravo(2, 22);
        emit Bravo(3, 33);
        emit Charlie(4, "44");
        emit Delta(5, 55, "555");
    }
}
