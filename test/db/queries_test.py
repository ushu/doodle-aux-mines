from fastapi.testclient import TestClient
import pytest
from db.models import Chain
from db.queries import get_active_chains
from main import app
from test.conftest import test_database

@pytest.mark.asyncio
async def test_empty_chains_dont_count(empty_chain: Chain):
    active_chains = await get_active_chains(test_database)
    assert len(active_chains) == 0

@pytest.mark.asyncio
async def test_with_valid_chain(
    empty_chain: Chain, 
    chain_with_two_elements: Chain):
    active_chains = await get_active_chains(test_database)
    assert len(active_chains) == 1
    # only the chain with two elements is returned by this query
    assert active_chains[0].id == chain_with_two_elements.id

@pytest.mark.asyncio
async def test_with_three_chains(
    empty_chain: Chain, 
    chain_with_two_elements: Chain,
    chain_with_three_elements: Chain
    ):
    active_chains = await get_active_chains(test_database)
    assert len(active_chains) == 1
    # only the chain with two elements is returned by this query
    # *not* the chain with three elements ! (it's last element is a text, not a drawing)
    assert active_chains[0].id == chain_with_two_elements.id