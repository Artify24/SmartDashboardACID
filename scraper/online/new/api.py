from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import asyncio
import logging
from functools import partial
from datetime import datetime
from save_raw_scraper import save_raw_scraper


# Import your existing scraping logic
from main import scrape_business

app = FastAPI(
    title="Business Intelligence Scraper API",
    description="API for scraping business websites and social media intelligence",
    version="1.0.0"
)

# -------------------------------------------------------------------
# CORS Configuration - Allow specific origins only
# -------------------------------------------------------------------
allowed_origins = [
    "http://localhost:3000",      # Frontend dev
    "http://localhost:8000",      # API dev
    "http://127.0.0.1:3000",      # Frontend localhost
    "http://127.0.0.1:8000",      # API localhost
    # Add your production domains here:
    # "https://yourdomain.com",
    # "https://www.yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Only these origins can access the API
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600  # Cache preflight requests for 1 hour
)

# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

# -------------------------------------------------------------------
# Request Model
# -------------------------------------------------------------------
class ScrapeRequest(BaseModel):
    """
    Accept either a full URL or just a business name.
    """
    url_or_name: str = Field(..., description="Website URL or business name to scrape")
    is_our_site: bool = Field(
        default=False,
        description="True if this scrape is for our own site, False if competitor"
    )
    max_pages: int = Field(default=20, ge=1, le=100, description="Maximum number of pages to scrape")
    headless: bool = Field(default=True, description="Run browser in headless mode")
    include_social: bool = Field(default=True, description="Include social media scraping")
    twitter: Optional[str] = Field(default=None, description="Twitter handle override")
    instagram: Optional[str] = Field(default=None, description="Instagram handle override")
    reddit: Optional[str] = Field(default=None, description="Reddit username override")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn company name override")

    class Config:
        json_schema_extra = {
            "example": {
                "url_or_name": "LeadSquared",
                "is_our_site": False,
                "max_pages": 5,
                "headless": True,
                "include_social": True
            }
        }

# -------------------------------------------------------------------
# Health Check
# -------------------------------------------------------------------
@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Scraper API is running"
    }

# -------------------------------------------------------------------
# Scrape Endpoint
# -------------------------------------------------------------------
@app.post("/scrape")
async def scrape_endpoint(request: ScrapeRequest):
    """
    Initiate a scraping job by URL or business name.
    """
    logger.info(
        f"Received scrape request for: {request.url_or_name} "
        f"(our_site={request.is_our_site})"
    )

    try:
        loop = asyncio.get_running_loop()

        scrape_func = partial(
            scrape_business,
            url=request.url_or_name,  # scraper handles name or URL
            max_pages=request.max_pages,
            headless=request.headless,
            output_dir="output",
            include_social=request.include_social,
            twitter=request.twitter,
            instagram=request.instagram,
            reddit=request.reddit,
            linkedin=request.linkedin
        )

        result = await loop.run_in_executor(None, scrape_func)

        if not isinstance(result, dict):
            raise HTTPException(status_code=500, detail="Invalid scraper response")

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        # -------------------------------------------------------------------
        # Response with site classification
        # -------------------------------------------------------------------
        response = {
            "target": request.url_or_name,
            "is_our_site": request.is_our_site,
            "scraped_at": datetime.utcnow().isoformat(),
            "data": result
        }
        save_raw_scraper(
            target=request.url_or_name,
            is_our_site=request.is_our_site,
            raw_json=response
        )
        return response

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("Scraping error")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during scraping"
        )

# -------------------------------------------------------------------
# Local Run
# -------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
