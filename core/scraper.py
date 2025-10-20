import asyncio
from playwright.async_api import async_playwright
from core.parser import parse_redfin_property


async def scrape_redfin(location: str):
    '''
    Scrape redfin for real estate listings in the given location.
    '''

    print(f"🔍 Scraping Redfin for location: {location}",end='\n')

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True,slow_mo=100)

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
               "AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en-US",
        )

        page = await context.new_page()

        properties = []

        try:
            # Go to redfin homepage and wait for searchbar to load
            await page.goto("https://www.redfin.com/",timeout=60000)
            await page.wait_for_selector('input#search-box-input',timeout=10000)

            # Switch to "Rent" section
            await page.locator('span[data-text="Rent"]').click()

            # Searh for the location
            search_box_placeholder = "City, Address, School, Building, ZIP"
            await page.get_by_placeholder(search_box_placeholder).click()
            await page.get_by_placeholder(search_box_placeholder).fill(location)
            await page.keyboard.press("Enter")
            
            print(f"➡️ Navigated to search results page for {location}",end='\n')

            # Wait for the listings to load
            await page.wait_for_selector("div.HomeCardContainer",timeout=20000)

            # Get HTML content of the page
            html_content = await page.content()
            properties = parse_redfin_property(html_content)
            print(f"✅ Scraped {len(properties)} properties from Redfin",end='\n')

        except Exception as e:
            print(f"⚠️ Scraper error: {e}",end='\n')

        finally:
            await browser.close()
        
        return properties
    

async def get_starting_url(location: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True,slow_mo=100)

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en-US",
        )

        page = await context.new_page()

        url = ""

        try:
            # Go to redfin homepage and wait for searchbar to load
            await page.goto("https://www.redfin.com/",timeout=60000)
            await page.wait_for_selector('input#search-box-input',timeout=10000)

            # Switch to "Rent" section
            await page.locator('span[data-text="Rent"]').click()

            # Searh for the location
            search_box_placeholder = "City, Address, School, Building, ZIP"
            await page.get_by_placeholder(search_box_placeholder).click()
            await page.get_by_placeholder(search_box_placeholder).fill(location)

            async with page.expect_navigation(wait_until="domcontentloaded", timeout=15000):
                await page.keyboard.press("Enter")
            
            # Get the current URL
            url = page.url

           

        except Exception as e:
            print(f"⚠️ Scraper error: {e}",end='\n')

        finally:
            await browser.close()

    return url