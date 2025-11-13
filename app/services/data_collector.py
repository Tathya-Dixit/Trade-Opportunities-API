from ddgs import DDGS
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class DataCollector:
    def __init__(self):
        self.ddgs = DDGS()

    async def collect_sector_data(self, sector: str) -> List[Dict]:
        try:
            query = f"India {sector} market latest news trends 2024 2025"

            results = self.ddgs.news(query, max_results=5)

            formatted_results = []
            for result in results:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "source": result.get("source", ""),
                    "date": result.get("date", ""),
                    "summary": result.get("body", ""),
                    "url": result.get("url", "")
                })

            logger.info(f"Collected {len(formatted_results)} articles for {sector}")
            return formatted_results

        except Exception as e:
            logger.error(f"Error collecting data: {str(e)}")
            return []
