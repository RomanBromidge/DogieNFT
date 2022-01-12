import pytest
from brownie import network
from scripts.simple_collectible.deploy_and_create import deploy_and_create
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("This test requires a local blockchain")
    simple_collectible = deploy_and_create()
    assert simple_collectible.ownerOf(0) == get_account()
