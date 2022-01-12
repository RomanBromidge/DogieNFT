from brownie import network, AdvancedCollectible
import pytest
import time
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    get_account,
    get_breed,
)
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible_integration():
    # deploy the contract
    # create an NFT
    # get a random breed back
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for testnet integration testing")
    # Act
    advanced_collectible, creation_transaction = deploy_and_create()
    # Wait for the testnet to verify the transaction
    time.sleep(180)
    # Assert
    assert advanced_collectible.tokenCounter() == 1


def test_get_breed():
    # Arrange / Act
    breed = get_breed(0)
    # Assert
    assert breed == "PUG"
