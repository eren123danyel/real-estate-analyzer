from playwright.async_api import async_playwright
from core.parser import parse_redfin_property
from ai.utils import extract_locations

# Get centralized logger
import logging

log = logging.getLogger(__name__)


async def scrape_redfin(location: str, max_price: int | None = None):
    """
    Scrape redfin for real estate listings in the given location.
    """
    try:
        location = extract_locations(location)[0]
    except Exception as e:
        log.error("⚠️ Invalid location!", e)
        return

    log.info(f"🕷️ Crawling Redfin for location: {location}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=100)

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
            await page.goto("https://www.redfin.com/", timeout=60000)
            await page.wait_for_load_state("networkidle")
            await page.wait_for_selector("input#search-box-input", timeout=10000)

            # Switch to "Rent" section
            await page.locator('span[data-text="Rent"]').click()

            # Search for the location
            search_box_placeholder = "City, Address, School, Building, ZIP"
            await page.wait_for_selector("input#search-box-input", timeout=10000)
            await page.get_by_placeholder(search_box_placeholder).click(timeout=10000)
            await page.get_by_placeholder(search_box_placeholder).fill(location)
            await page.keyboard.press("Enter")
            await page.wait_for_load_state("networkidle")

            log.info(f"➡️  Navigated to search results page for {location}")

            # Wait for the listings to load
            await page.wait_for_selector("div.HomeCardContainer", timeout=20000)

            # Get HTML content of the page
            html_content = await page.content()
            properties = parse_redfin_property(html_content, max_price)
            log.info(f"✅ Scraped {len(properties)} properties from Redfin")

        except Exception as e:
            if "ERR_NAME_NOT_RESOLVED" in str(e):
                log.error(
                    "⚠️  Network error: Unable to resolve domain. Please check your internet connection."
                )
                return
            else:
                log.warning(f"⚠️  Scraper error: {e}")
            raise e

        finally:
            await browser.close()

        return properties


async def get_starting_url(location: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=100)

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
            await page.goto("https://www.redfin.com/", timeout=60000)
            await page.wait_for_load_state("networkidle")
            await page.wait_for_selector("input#search-box-input", timeout=10000)

            # Switch to "Rent" section
            await page.locator('span[data-text="Rent"]').click()

            # Search for the location
            search_box_placeholder = "City, Address, School, Building, ZIP"
            await page.wait_for_selector("input#search-box-input", timeout=10000)
            await page.get_by_placeholder(search_box_placeholder).click(timeout=10000)
            await page.get_by_placeholder(search_box_placeholder).fill(location)
            await page.keyboard.press("Enter")
            await page.wait_for_load_state("networkidle")

            # Wait for the listings to load to ensure we are on the correct page
            await page.wait_for_selector("div.HomeCardContainer", timeout=20000)

            # Get the current URL
            url = page.url

        except Exception as e:
            if "ERR_NAME_NOT_RESOLVED" in str(e):
                log.error(
                    "⚠️  Network error: Unable to resolve domain. Please check your internet connection."
                )
                return
            else:
                log.warning(f"⚠️  Scraper error: {e}")
            raise e

        finally:
            await browser.close()

    return url
