import uvicorn
from fastapi import FastAPI, Query
from ai.mcp_client import run_redfin_scraper
from ai.utils import extract_locations
from core.scraper import scrape_redfin, get_starting_url

app = FastAPI(
    title="Real Estate Rent Analyzer API",
    description="Playwright-powered property scraping and AI automation.",
    version="1.0.0",
)

@app.get("/search_redfin_with_ai")
async def run_task_endpoint(goal: str = Query(..., description="Natural language goal, e.g. 'Find rent under 3000 in Los Angeles'")):
    location = extract_locations(goal)
    if not location:
        return {"status": "error", "message": "Could not extract location from the goal. Please specify a valid location."}
    try:
        start_url = await get_starting_url(location[0])
    except Exception as e:
        return {"status": "error", "message": f"Failed to get starting URL. {str(e)}"}
    
    listings = await run_redfin_scraper(goal, start_url)

    if listings:
        return {"status": "success", "count": len(listings), "properties": listings}
    else:
        return {"status": "error", "message": "No listings found."}

@app.get("/search_redfin")
async def search_redfin(location: str = Query(..., description="Location to scrape properties"), max_price: int = Query(None, description="Max price that the properties can have (leave blank for unlimited)")):
    listings = await scrape_redfin(location, max_price)

    if listings:
        return {"status": "success", "count": len(listings), "properties": listings}
    else: 
        return {"status": "error", "message": "No listings found."}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)