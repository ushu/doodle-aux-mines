import datetime
from typing import Literal
from pydantic import BaseModel

class Chain(BaseModel):
    id: int
    is_active: bool
    created_at: datetime.datetime

class ChainElement(BaseModel):
    id: int
    chain_id: int
    order_number: int
    content: str
    type: Literal["text", "drawing"]
    player_name: str
    created_at: datetime.datetime

class ChainInfoSummary(BaseModel):
    id: int
    last_type: Literal["text", "drawing"]
    last_content: str
    players_count: int
    turns_count: int

class AvailableChainInfo(BaseModel):
    id: int
    last_type: Literal["text", "drawing"]
    last_content: str
    last_order: int

class ChainHistoryEntry(BaseModel):
    order_number: int
    type: Literal["text", "drawing"]
    content: str
    player_name: str
    created_at: datetime.datetime
