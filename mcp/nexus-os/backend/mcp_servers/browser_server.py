from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright
import asyncio

mcp = FastMCP("browser")

@mcp.tool()
async def open_website(url: str):
    """Open a website and return its text content."""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            content = await page.content()
            await browser.close()
            # In a real scenario, you'd extract specific text or markdown.
            # Here we just return a success message or snippet to avoid large payloads.
            return f"Successfully opened {url}. Page length: {len(content)} chars."
    except Exception as e:
        return f"Failed to open {url}. Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
