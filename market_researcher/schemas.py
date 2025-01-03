#!/usr/bin/env python
from pydantic import BaseModel
from typing import List, Optional

class MarketResearchInput(BaseModel):
    ticker_symbols: List[str]
    max_news_sources: int = 5
    research_depth: str = "brief"

class InputSchema(BaseModel):
    tool_name: str
    tool_input_data: MarketResearchInput