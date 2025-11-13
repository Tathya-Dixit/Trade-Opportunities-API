import google.generativeai as genai
import os
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class AIAnalyzer:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def analyze_market_data(self, sector: str, data: List[Dict]) -> str:
        try:
            data_summary = self._format_data_for_analysis(data)

            prompt = f"""
You are a market analyst specializing in Indian markets. Analyze the following market data for the {sector} sector in India.

Collected Market Data:
{data_summary}

Please provide a comprehensive markdown report with the following sections:

# {sector.title()} Sector - Market Analysis Report

## 1. Executive Summary
Provide a brief overview of the current state of the sector.

## 2. Market Overview
Describe the current market conditions, size, and growth trajectory.

## 3. Current Trends
List and explain the major trends shaping this sector.

## 4. Trade Opportunities
Identify specific opportunities for businesses and investors.

## 5. Key Players
Mention major companies and their market positions.

## 6. Challenges and Risks
Outline potential challenges and risk factors.

## 7. Recommendations
Provide actionable recommendations for stakeholders.

## 8. Sources
List the news sources referenced in this analysis.

Make the report professional, data-driven, and actionable.
"""

            response = self.model.generate_content(prompt)

            logger.info(f"Successfully analyzed data for {sector}")
            return response.text

        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            return f"# Error\n\nUnable to generate analysis: {str(e)}"

    def _format_data_for_analysis(self, data: List[Dict]) -> str:
        if not data:
            return "No recent data available."

        formatted = []
        for i, item in enumerate(data, 1):
            formatted.append(f"""
Article {i}:
- Title: {item['title']}
- Source: {item['source']}
- Date: {item['date']}
- Summary: {item['summary']}
""")

        return "\n".join(formatted)
