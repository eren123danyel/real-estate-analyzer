import argparse
from logging_setup import setup_logging
import logging

setup_logging()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Analyze rental prices in a given area.")

parser.add_argument("-o","--output", type=str, default=None,
                    help="Output CSV file to save rental analysis results (default: will output to terminal)")

parser.add_argument("-l","--location", type=str, default=None,
                    help="Area ('City, State', Address or ZIP) to analyze rental prices")

parser.add_argument("-m","--max_price", type=int, default=None,
                    help="Maximum rental price to filter properties")

parser.add_argument("-ai","--use_ai", action="store_true", help="Use AI-powered scraping for enhanced results with playwright MCP server that allows user to specify specifc criteria like (Must use --goal flag and have OPENAI_API_KEY set in .env)")

parser.add_argument("-g","--goal", type=str, default=None,
                    help="Natural language goal for AI-powered scraping (e.g., 'Find 2-bedroom apartments under $2500 in Seattle, WA')")

parser.add_argument("-api","--server-api", action="store_true", help="Host Fast API endpoint for external access (Will ignore other flags)")


args = parser.parse_args()


if __name__ == "__main__":
    if args.server_api:
        from api.server import main
        main()

    elif args.use_ai:
        from ai.mcp_client import run_scraper_with_shutdown, get_starting_url
        from ai.utils import extract_locations
        from dotenv import dotenv_values
        import asyncio

        async def main():
            if not dotenv_values(".env")["OPENAI_API_KEY"]:
                log.error("❌ OPENAI_API_KEY not set in .env file. Please set it to use AI-powered scraping.")
                return
            
            if not args.goal:
                log.error("❌ Please provide a natural language goal using the --goal flag for AI-powered scraping.")
                return

            location = extract_locations(args.goal)

            if not location:
                log.error("❌ Could not extract location from the input. Please specify a valid location in user goal.")
                return
            
            try:
                start_url = await get_starting_url(location[0])
            except Exception as e:
                if "ERR_NAME_NOT_RESOLVED" in str(e):
                    log.error("⚠️  Network error: Unable to resolve domain. Please check your internet connection.")
                    return
                else:
                    log.error("Please ensure the location is valid and try again.")
                    return

            listings = await run_scraper_with_shutdown(args.goal, start_url)

            if not listings:
                log.error("❌ No properties found matching the criteria.")
            else:
                log.info(f"✅ Found {len(listings)} properties matching criteria.")
                if args.output:
                    import csv
                    keys = listings[0].keys()
                    with open(args.output, 'w', newline='', encoding='utf-8') as output_file:
                        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                        dict_writer.writeheader()
                        dict_writer.writerows(listings)
                    log.info(f"✅ Listings saved to {args.output}")
                else:
                    for idx, listing in enumerate(listings, start=1):
                        print(f"{idx}. {listing['address']} - {listing['price']} - {listing['beds']} beds - {listing['baths']} baths - link: {listing['link']}")
                    

        asyncio.run(main())

    else:
        from core.scraper import scrape_redfin
        import asyncio

        async def main():
            listings = await scrape_redfin(args.location, args.max_price)

            if not listings:
                log.error("❌ No listings found.")
                return
            
            log.info(f'✅ Found {len(listings)} listings:')

            if args.output:
                import csv
                keys = listings[0].keys()
                with open(args.output, 'w', newline='', encoding='utf-8') as output_file:
                    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(listings)
                log.info(f"💾 Listings saved to {args.output}", )
            else:
                for idx, listing in enumerate(listings, start=1):
                    print(f"{idx}. {listing['address']} - {listing['price']} - {listing['beds']} beds - {listing['baths']} baths - link: {listing['link']}")

        asyncio.run(main())