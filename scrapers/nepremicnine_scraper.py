import asyncio
import logging
import psycopg2
from pyppeteer import launch
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_urls_from_db():
    # Database connection parameters
    conn_params = {
        'dbname': 'real_estate',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost'
    }

    # Connect to the database
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()

    # Fetch URLs from the database
    cur.execute("SELECT url FROM urls")
    urls = [row[0] for row in cur.fetchall()]

    # Close the connection
    cur.close()
    conn.close()

    return urls

async def scrape_data(url, browser):
    try:
        page = await browser.newPage()
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        await page.goto(url)
        await page.waitForSelector('a.url-title-d', {'timeout': 60000})  # Increased timeout to 60 seconds

        # Find all elements with the class "url-title-d"
        links = await page.querySelectorAll('a.url-title-d')

        for link in links:
            try:
                # Click on the link to go to the detailed page
                await link.click()

                # Wait for the detailed page to load
                await page.waitForSelector('h1.listing-title', {'timeout': 60000})  # Increased timeout to 60 seconds

                # Get page content and parse it with BeautifulSoup
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')

                title = soup.find('h1', class_='listing-title').text.strip() if soup.find('h1', class_='listing-title') else None
                price = soup.find('span', class_='listing-price').text.strip() if soup.find('span', class_='listing-price') else None
                location = soup.find('div', class_='listing-location').text.strip() if soup.find('div', class_='listing-location') else None

                # Scrape breadcrumb data
                breadcrumbs = soup.find('ul', class_='breadcrumbs')
                breadcrumb_items = breadcrumbs.find_all('li') if breadcrumbs else []

                breadcrumb_data = [item.find('span', itemprop='name').text.strip() for item in breadcrumb_items]
                type_ = breadcrumb_data[0] if len(breadcrumb_data) > 0 else None
                location_ = breadcrumb_data[1] if len(breadcrumb_data) > 1 else None
                object_type = breadcrumb_data[2] if len(breadcrumb_data) > 2 else None
                object_size = breadcrumb_data[3] if len(breadcrumb_data) > 3 else None

                # Save the scraped data
                await save_scraped_data({
                    'url': page.url,
                    'title': title,
                    'price': price,
                    'location': location,
                    'type': type_,
                    'breadcrumb_location': location_,
                    'object_type': object_type,
                    'object_size': object_size
                })

                logger.info(f"Successfully scraped data from {page.url}")

                # Go back to the original page
                await page.goBack()
                await page.waitForSelector('a.url-title-d', {'timeout': 60000})  # Re-wait for the original page

            except Exception as e:
                logger.error(f"Failed to scrape data from link: {e}")
                await page.goBack()
                await page.waitForSelector('a.url-title-d', {'timeout': 60000})  # Re-wait for the original page

    except Exception as e:
        logger.error(f"Failed to scrape URL {url}: {e}")

async def save_scraped_data(data):
    # Database connection parameters
    conn_params = {
        'dbname': 'real_estate',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost'
    }

    # Connect to the database
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS scraped_data (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            title TEXT,
            price TEXT,
            location TEXT,
            type TEXT,
            breadcrumb_location TEXT,
            object_type TEXT,
            object_size TEXT
        )
    """)

    # Insert scraped data into the table
    cur.execute("""
        INSERT INTO scraped_data (url, title, price, location, type, breadcrumb_location, object_type, object_size) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (data['url'], data['title'], data['price'], data['location'], data['type'], data['breadcrumb_location'], data['object_type'], data['object_size']))

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()

async def main():
    browser = await launch(headless=True)
    urls = await get_urls_from_db()

    for url in urls:
        await scrape_data(url, browser)

    await browser.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
