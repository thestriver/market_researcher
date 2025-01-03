#!/usr/bin/env python
from dotenv import load_dotenv
import os
import requests
from naptha_sdk.schemas import AgentRunInput
from naptha_sdk.utils import get_logger
from pydantic import BaseModel
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from market_researcher.schemas import MarketResearchInput, InputSchema

load_dotenv()
logger = get_logger(__name__)

print("OpenAI Key loaded:", bool(os.getenv("OPENAI_API_KEY")))

class MarketResearchAnalyst:
    def __init__(self, module_run):
        self.module_run = module_run
        self.llm_config = module_run.deployment.config.llm_config
        self.setup_llm()
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json"
        }

    def setup_llm(self):
        """Initialize LLM configuration"""
        self.llm = ChatOpenAI(
            model_name=self.llm_config.model,
            temperature=self.llm_config.temperature
        )

    def search_news(self, query: str) -> List[Dict]:
        url = "https://google.serper.dev/news"
        payload = {"q": query}
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json().get("news", [])[:self.max_news_sources]

    def search_analysis(self, query: str) -> Dict:
        url = "https://google.serper.dev/search"
        payload = {"q": query}
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def research_company(self, symbol: str, max_sources: int) -> Dict:
        news_results = self.search_news(f"{symbol} stock news latest developments")
        analysis_results = self.search_analysis(f"{symbol} market analysis industry trends competitors")

        prompt = f"""
        Based on this information about {symbol}:
        
        News:
        {news_results}
        
        Market Analysis:
        {analysis_results}
        
        Provide a detailed research report covering:
        1. Key recent developments
        2. Market trends
        3. Competitive position
        4. Industry outlook
        5. Risks and opportunities
        """
        
        response = self.llm.invoke(prompt)
        
        return {
            "news_summary": news_results,
            "market_analysis": analysis_results,
            "research_report": response.content
        }

    def analyze(self, input_data: MarketResearchInput) -> Dict[str, Any]:
        try:
            self.max_news_sources = input_data.max_news_sources
            results = {}
            for symbol in input_data.ticker_symbols:
                results[symbol] = self.research_company(symbol, input_data.max_news_sources)
            return results
        except Exception as e:
            logger.error(f"Research failed: {str(e)}")
            raise

def run(module_run, *args, **kwargs):
    """Main entry point for the market researcher"""
    researcher = MarketResearchAnalyst(module_run)
    
    if isinstance(module_run.inputs, dict):
        input_params = InputSchema(**module_run.inputs)
    else:
        input_params = module_run.inputs
        
    return researcher.analyze(input_params.tool_input_data)

if __name__ == "__main__":
    import asyncio
    from naptha_sdk.client.naptha import Naptha
    from naptha_sdk.configs import setup_module_deployment

    naptha = Naptha()

    deployment = asyncio.run(setup_module_deployment(
        "agent", 
        "market_researcher/configs/deployment.json",
        node_url=os.getenv("NODE_URL")
    ))

    input_params = InputSchema(
        tool_name="analyze",
        tool_input_data=MarketResearchInput(
            ticker_symbols=["AAPL"],
            max_news_sources=5,
            research_depth="comprehensive"
        )
    )

    module_run = AgentRunInput(
        inputs=input_params,
        deployment=deployment,
        consumer_id=naptha.user.id,
    )

    response = run(module_run)
    print("\nMarket Research Results:")
    print("=========================")
    print(response)