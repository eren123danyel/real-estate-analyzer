import uvicorn
from fastapi import FastAPI, Query
from ai.mcp_client import run_redfin_scraper, get_mcp_server, shutdown_mcp
from ai.utils import extract_locations
from core.scraper import scrape_redfin, get_starting_url
from contextlib import asynccontextmanager

# Get centralized logger
import logging

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On start up
    await get_mcp_server()
    yield
    # On exit
    await shutdown_mcp()


app = FastAPI(
    title="Real Estate Rent Analyzer API",
    description="Playwright-powered property scraping and AI automation.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/search_redfin_with_ai")
async def run_task_endpoint(
    goal: str = Query(
        ...,
        description="Natural language goal, e.g. 'Find rent under 3000 in Los Angeles'",
    ),
):
    # Get the location from the goal
    location = extract_locations(goal)

    # If we cant find the location in the string we want to return an error
    if not location:
        return {
            "status": "error",
            "message": "Could not extract location from the goal. Please specify a valid location.",
        }

    # We try to get rental page where we can apply filters
    try:
        start_url = await get_starting_url(location[0])
    except Exception as e:
        return {"status": "error", "message": f"Failed to get starting URL. {str(e)}"}

    # We run the LLM and wait for to finish
    listings = await run_redfin_scraper(goal, start_url)

    # If listings were found, return success and the properties. Else give an error
    if listings:
        return {"status": "success", "count": len(listings), "properties": listings}
    else:
        return {"status": "error", "message": "No listings found."}


@app.get("/search_redfin")
async def search_redfin(
    location: str = Query(..., description="Location to scrape properties"),
    max_price: int = Query(
        None,
        description="Max price that the properties can have (leave blank for unlimited)",
    ),
):
    # Wait for manual scraping of site
    listings = await scrape_redfin(location, max_price)

    # If listings were found, return success and the properties. Else give an error
    if listings:
        return {"status": "success", "count": len(listings), "properties": listings}
    else:
        return {"status": "error", "message": "No listings found."}


def main():
    # Run app on port 8080
    uvicorn.run(app, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    main()
