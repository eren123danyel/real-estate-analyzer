import logging
import asyncio
from core.scraper import scrape_redfin

logger = logging.getLogger(__name__)
logging.basicConfig(filename="real-estate-analyzer.log",level=logging.INFO)


async def main():
    location = input("Enter location (City,State or ZIP) to scrape properties: ").strip()
    listings = await scrape_redfin(location)

    if not listings:
        print("❌ No listings found.",end='\n')
        return
    
    print(f'✅ Found {len(listings)} listings:',end='\n')

    for idx, listing in enumerate(listings, start=1):
        print(f"{idx}. {listing['address']} - {listing['price']} - {listing['beds']} beds - {listing['baths']} baths - link: {listing['link']}",end='\n')



if __name__ == "__main__":
    asyncio.run(main())