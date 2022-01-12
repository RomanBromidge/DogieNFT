// An NFT is a ERC 721 compliant token!

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// import "@openzeppelin/contracts/token/ERC721/ERC721.sol"; unnecessary as parent to ERC721URIStorage, so gets imported automatically
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

// This is a factory contract that creates NFTs. It creates many NFTs, but they are all sorted in this one contract
contract SimpleCollectible is ERC721URIStorage {
    uint256 public tokenCounter;

    constructor() public ERC721("Dogie", "DOG") {
        tokenCounter = 0;
    }

    function createCollectible(string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
        return newTokenId;
    }
}
