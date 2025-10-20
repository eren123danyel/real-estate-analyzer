import logging
import asyncio
from core.scraper import scrape_redfin
from ai.mcp_client import run_redfin_scraper, get_starting_url
from ai.utils import extract_locations

logger = logging.getLogger(__name__)
logging.basicConfig(filename="real-estate-analyzer.log",level=logging.INFO)


async def main():
    menu = input("""
🏠 Real Estate Rent Analyzer
                
Pick from the following options:
1. Scrape Redfin for property listings (w/o AI)
2. Scrape Redfin for properties with AI and Playwright MCP

Enter option (1 or 2) >""").strip()

    if menu == "1":
        location = input("Enter location (City, State or ZIP) to scrape properties: ").strip()

        while not location:
            location = input("Please enter a valid location (City, State or ZIP): ").strip()

        max_price = input("Enter maximum price (or leave blank for no limit): ").strip()

        while not max_price.isdigit():
            if not max_price:
                break
            else:
                max_price = input("Please enter a valid maximum price (or leave blank for no limit): ").strip()
        
        listings = await scrape_redfin(location)

        if not listings:
            print("❌ No listings found.",end='\n')
            return
        
        print(f'✅ Found {len(listings)} listings:',end='\n')

        for idx, listing in enumerate(listings, start=1):
            print(f"{idx}. {listing['address']} - {listing['price']} - {listing['beds']} beds - {listing['baths']} baths - link: {listing['link']}",end='\n')

    if menu == "2":
        user_goal = input("Enter your property search goal (e.g., 'Find 2-bedroom apartments under $2500 in Seattle, WA with 2 bedrooms'): ").strip()
        
        while not user_goal:
            user_goal = input("Please enter a valid property search goal: ").strip()
        
        location = extract_locations(user_goal)

        if not location:
            print("❌ Could not extract location from the goal. Please specify a valid location.",end='\n')
            return
        
        try:
            start_url = await get_starting_url(location[0])
        except Exception as e:
            print(f"❌ Failed to get starting URL: {e}", end="\n")
            print("Please ensure the location is valid and try again.", end="\n")
            return

        properties = await run_redfin_scraper(user_goal, start_url)

        if not properties:
            print("❌ No properties found matching the criteria.", end="\n")
        else:
            print(f"✅ Found {len(properties)} properties matching criteria.", end="\n")
            for idx, listing in enumerate(properties, start=1):
                print(f"{idx}. {listing['address']} - {listing['price']} - {listing['beds']} beds - {listing['baths']} baths - link: {listing['link']}")

if __name__ == "__main__":
    asyncio.run(main())