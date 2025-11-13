from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime
import logging

from app.services.data_collector import DataCollector
from app.services.ai_analyzer import AIAnalyzer
from app.middleware.auth import verify_token, create_access_token, verify_credentials
from app.middleware.rate_limiter import rate_limiter
from app.models.schemas import AnalysisResponse, Token

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Trade Opportunities API",
    description="Analyze market data and provide trade opportunity insights for Indian sectors",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_collector = DataCollector()
ai_analyzer = AIAnalyzer()



@app.get("/")
async def root():
    return {
        "message": "Trade Opportunities API is running",
        "docs": "/docs",
        "login": "/token",
        "analyze_sector": "/analyze/{sector}"
    }



@app.post("/token", response_model=Token)
async def login(username: str, password: str):
    """
    Login endpoint to get access token

    Demo users:
    - username: demo, password: demo123
    - username: guest, password: guest123
    """
    if not verify_credentials(username, password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(username)
    return {"access_token": access_token, "token_type": "bearer"}



@app.get("/analyze/{sector}", response_model=AnalysisResponse)
async def analyze_sector(sector: str, username: str = Depends(verify_token)):
    """
    Analyze a specific sector and return market insights

    Parameters:
    - sector: Name of the sector (e.g., pharmaceuticals, technology, agriculture)

    Returns:
    - Markdown formatted market analysis report
    """
    try:
        await rate_limiter.check_rate_limit(username)

        sector = sector.lower().strip()
        if len(sector) < 3 or len(sector) > 50:
            raise HTTPException(status_code=400, detail="Invalid sector name")

        logger.info(f"User {username} requested analysis for sector: {sector}")

        logger.info("Collecting market data...")
        market_data = await data_collector.collect_sector_data(sector)

        if not market_data:
            raise HTTPException(
                status_code=404,
                detail="No recent market data found for this sector"
            )

        logger.info("Analyzing data with AI...")
        report = await ai_analyzer.analyze_market_data(sector, market_data)

        return AnalysisResponse(
            sector=sector,
            report=report,
            timestamp=datetime.utcnow().isoformat(),
            sources_count=len(market_data)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing sector: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")
