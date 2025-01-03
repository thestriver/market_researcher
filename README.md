# Market Researcher

A sophisticated market research analyst module for Naptha that provides detailed market analysis and news insights for stocks. This module uses Google Search API (via Serper) to gather latest news and market analysis, and processes it using OpenAI's language models to generate comprehensive research reports.

## Features

- Fetches latest news about specified stocks
- Gathers market analysis and industry trends
- Provides detailed research reports covering:
  - Key recent developments
  - Market trends
  - Competitive position
  - Industry outlook
  - Risks and opportunities

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/market-researcher.git
cd market-researcher
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file with your API keys:
```bash
SERPER_API_KEY=your_serper_api_key
OPENAI_API_KEY=your_openai_api_key
NODE_URL=your_node_url
```

## Local Testing

Run the module locally:
```bash
poetry run python market_researcher/run.py
```

## Deployment

1. Push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit: Market Researcher module"
git remote add origin https://github.com/YourUsername/market-researcher.git
git push -u origin main
git tag v0.1
git push origin v0.1
```

2. Create the Naptha agent:
```bash
naptha agents market-researcher -p "description='A sophisticated market research analyst that provides detailed market analysis and news insights for stocks' parameters='{tool_name: str, tool_input_data: {ticker_symbols: List[str], max_news_sources: int, research_depth: str}}' module_url='https://github.com/YourUsername/market-researcher' module_version='v0.1'"
```

## Usage

Run the agent using the Naptha CLI:
```bash
naptha run agent:market-researcher -p '{
    "tool_name": "analyze",
    "tool_input_data": {
        "ticker_symbols": ["AAPL"],
        "max_news_sources": 5,
        "research_depth": "comprehensive"
    }
}'
```

## Input Parameters

- `ticker_symbols`: List of stock ticker symbols to analyze
- `max_news_sources`: Maximum number of news sources to fetch (default: 5)
- `research_depth`: Depth of analysis ("basic" or "comprehensive")

## Dependencies

- Python >=3.10,<=3.13
- naptha-sdk
- python-dotenv
- langchain-openai
- pydantic
- requests

```
