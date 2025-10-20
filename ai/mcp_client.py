import os
import asyncio
import json
from dotenv import dotenv_values
from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServerStdio
from core.parser import parse_redfin_property
from core.scraper import get_starting_url
from ai.utils import extract_tool_output, extract_locations

# Load API key
os.environ["OPENAI_API_KEY"] = dotenv_values(".env")["OPENAI_API_KEY"]
mcp_instance = None  # Global MCP server instance

async def get_mcp_server():
    """
    Initialize and return a running Playwright MCP server context manager.
    Use this in an async with block.
    """

    
    userAgent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
    )
    

    global mcp_instance
    if mcp_instance is None:
        print("🚀 Launching global MCP server...", end="\n")

        mcp_instance = MCPServerStdio(
            name="Playwright",
            params={
                "command": "npx",
                "args": [
                    "@playwright/mcp@latest",
                    "--headless",
                    "--viewport-size", "1280,800",
                    "--user-agent", userAgent
                    ],
            },
            cache_tools_list=False,
            client_session_timeout_seconds=120
        )
        await mcp_instance.__aenter__()  # Start it once
        print("🏃 MCP server is running.",end="\n")
    return mcp_instance

async def shutdown_mcp():
    global mcp_instance
    if mcp_instance:
        print("🧹 Shutting down MCP server...")
        await mcp_instance.__aexit__(None, None, None)
        mcp_instance = None


async def run_redfin_scraper(user_criteria: str, start_url: str):
    """
    Main function to scrape Redfin based on user criteria.
    
    Args:
        user_criteria: String describing user criteria for filtering properties
        start_url: Starting Redfin URL
    """


    mcp = await get_mcp_server()

    try:
        # Navigation Agent - handles initial page load and filtering
        navigator = Agent(
            name="NavigatorAgent",
            model="gpt-5-mini",
            mcp_servers=[mcp],
            instructions=f"""You are a web navigation expert for Redfin.com.

            User Criteria:
            {json.dumps(user_criteria, indent=2)}

            Your task:
            1. Navigate ONCE to the starting URL.
            2. Apply filters based on the user criteria (price, beds, baths, etc.).
            3. Wait for results to load on the same page.
            4. DO NOT click pagination or navigate to new URLs.
            5. Once filters are applied and listings are visible, respond ONLY with: "FILTERS_APPLIED".

            Hard restrictions:
            - Never call browser_navigate() after the initial page load.
            - Never click pagination or external links.
            - Stay on the current DOM context at all times.

            Use any MCP browser tools as needed to accomplish this.

            Stop tool use immediately after filters are applied.
            """
        )

        trace_id = gen_trace_id()
        print(f"🔍 Trace URL: https://platform.openai.com/traces/trace?trace_id={trace_id}", end="\n")

        with trace(workflow_name="RedfinPropertyScraper", trace_id=trace_id):            
            print(f"📋 Search Criteria:", user_criteria, end="\n")
            print(f"🌐 Starting URL: {start_url}", end="\n")
            
            # Phase 1: Navigate and apply filters
            print("Phase 1: Navigating and applying filters...", end="\n")
            print("-" * 60, end="\n")
            
            nav_result = await Runner.run(
                starting_agent=navigator,
                input=f"Navigate to {start_url} and apply the filters from the user criteria.",
                max_turns=15,
            )
            
            print(f"\n✅ Navigation complete: {nav_result.final_output}\n")

            # Check if filters were applied
            if "FILTERS_APPLIED" not in nav_result.final_output:
                print("⚠️ Warning: Filters may not have been fully applied. Continuing anyway...")
            print("Phase 2: Scraping property listings...", end="\n")
            print("-" * 60, end="\n")

            # Phase 2: Get HTML and scrape property listings
            html_result = await mcp.call_tool("browser_evaluate", {
                "function": """async () => {
                document.querySelectorAll('script, style').forEach(el => el.remove());
                return document.documentElement.outerHTML;
                }"""
            })

            html = extract_tool_output(html_result)
        
            properties = parse_redfin_property(html)

            return properties
    except Exception as e:
        print(f"⚠️  Scraper error: {e}", end="\n")
        raise e
async def run_scraper_with_shutdown(user_goal, start_url):
        '''Ensure they are on the same thread'''
        result = ""
        try:
            result = await run_redfin_scraper(user_goal, start_url)
        except asyncio.CancelledError:
            raise
        finally:
            await shutdown_mcp()
            return result
            
if __name__ == "__main__":
    user_goal = input("Enter your property search goal (e.g., 'Find 2-bedroom apartments under $2500 in Seattle, WA'): ").strip()
    user_goal = user_goal if user_goal else "Collect all rental listings under $2500 with ≥2 beds and ≥1 bath in Seattle."
    location = extract_locations(user_goal)
    start_url = asyncio.run(get_starting_url(location[0]))

    

    asyncio.run(run_scraper_with_shutdown(user_goal,start_url))