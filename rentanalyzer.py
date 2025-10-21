import argparse
from logging_setup import setup_logging
import logging

# Get the shared logger
setup_logging()
log = logging.getLogger(__name__)


# Setup the arguments for CLI tool
parser = argparse.ArgumentParser(description="Analyze rental prices in a given area.")

parser.add_argument("-o","--output", type=str, default=None,
                    help="Output CSV file to save rental analysis results (default: will output to terminal)")

parser.add_argument("-l","--location", type=str, default=None,
                    help="Area ('City, State', Address or ZIP) to analyze rental prices")

parser.add_argument("-m","--max_price", type=int, default=None,
                    help="Maximum rental price to filter properties")

parser.add_argument("-g","--goal", type=str, default=None,
                    help="Use AI-powered scraping for Natural language goal with Playwright MCP server (e.g., 'Find 2-bedroom apartments under $2500 in Seattle, WA') (Use by itself, must have OPENAI_API_KEY set in .env)")

parser.add_argument("-api","--server-api", action="store_true", help="Host Fast API endpoint for external access (Will ignore other flags)")


args = parser.parse_args()


if __name__ == "__main__":
    # If run with -api, then start the server
    if args.server_api:
        from api.server import main
        main()

    # If run with -g flag, then try to run the LLM to retrieve the information
    elif args.goal:
        from ai.mcp_client import run_scraper_with_shutdown, get_starting_url
        from ai.utils import extract_locations
        from dotenv import dotenv_values
        import asyncio

        # Define main seperatly so we can run asyncio
        async def main():
            # If the is no OPENAI_API_KEY in .env, return an error
            if not dotenv_values(".env")["OPENAI_API_KEY"]:
                log.error("❌ OPENAI_API_KEY not set in .env file. Please set it to use AI-powered scraping.")
                return

            # Try to extract location from the goal
            location = extract_locations(args.goal)

            # If we couldnt find the location, return an error
            if not location:
                log.error("❌ Could not extract location from the input. Please specify a valid location in user goal.")
                return
            
            try:
                start_url = await get_starting_url(location[0])
            except Exception:
                log.error("❌ Could not get the starting URL, try a more specific location")
                return

            # Run the scraper and when finished, shutdown the MCP server
            listings = await run_scraper_with_shutdown(args.goal, start_url)

            # If there are no listings, give an error
            if not listings:
                log.error("❌ No properties found matching the criteria.")
            else:
                log.info(f"✅ Found {len(listings)} properties matching criteria.")

                # If user wants to save as a CSV
                if args.output:
                    import csv
                    keys = listings[0].keys()
                    with open(args.output, 'w', newline='', encoding='utf-8') as output_file:
                        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                        dict_writer.writeheader()
                        dict_writer.writerows(listings)
                    log.info(f"✅ Listings saved to {args.output}")
                else:
                # Else write to terminal
                    for idx, listing in enumerate(listings, start=1):
                        print(f"{idx}. {listing['address']} - {listing['price']} - {listing['beds']} beds - {listing['baths']} baths - link: {listing['link']}")
                    
        # Run main asynchrounsly 
        asyncio.run(main())

    # If the -l flag is specified
    elif args.location:
        from core.scraper import scrape_redfin
        import asyncio

        # Define main seperatly so we can run asyncio
        async def main():
            # Manually scrape listings
            listings = await scrape_redfin(args.location, args.max_price)

            # If there are no listings
            if not listings:
                log.error("❌ No listings found.")
                return
            
            log.info(f'✅ Found {len(listings)} listings:')

            # If user wants to save file as a CSV
            if args.output:
                import csv
                keys = listings[0].keys()
                with open(args.output, 'w', newline='', encoding='utf-8') as output_file:
                    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(listings)
                log.info(f"💾 Listings saved to {args.output}", )
            else:
            # Else write to terminal
                for idx, listing in enumerate(listings, start=1):
                    print(f"{idx}. {listing['address']} - {listing['price']} - {listing['beds']} beds - {listing['baths']} baths - link: {listing['link']}")

        asyncio.run(main())
    else:
        log.info("No arguments specified")