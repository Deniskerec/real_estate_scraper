import logging
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_driver():
    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def find_all_options(url):
    driver = setup_driver()
    driver.get(url)
    sleep(5)  # Allow time for the page to load

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    options_dict = {
        'p': {},
        'n': {},
        'r': {
            '14': 'lj-mesto',
            '1': 'lj-okolica',
            '3': 'gorenjska',
            '2': 'j-primorska',
            '4': 's-primorska',
            '8': 'notranjska',
            '5': 'savinjska',
            '9': 'podravska',
            '10': 'koroska',
            '6': 'dolenjska',
            '12': 'posavska',
            '11': 'zasavska',
            '15': 'pomurska'
        }
    }

    select_elements = soup.find_all('select')
    for select in select_elements:
        name = select.get('name')
        if name in options_dict:
            options = select.find_all('option')
            for option in options:
                value = option.get('value')
                text = replace_special_characters(option.text.lower())
                options_dict[name][value] = text

    driver.quit()
    return options_dict


def replace_special_characters(text):
    replacements = {
        'č': 'c',
        'š': 's',
        'ž': 'z',
        ' ': '-'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def print_tree(options_dict):
    for p_key, p_value in options_dict['p'].items():
        print(f"{p_value}:")
        for r_key, r_value in options_dict['r'].items():
            n_values = " ".join([n_value for n_key, n_value in options_dict['n'].items()])
            print(f"  {r_value}: {n_values}")


def generate_urls(options_dict):
    base_url = 'https://www.nepremicnine.net/oglasi'
    urls = []
    for p_key, p_value in options_dict['p'].items():
        for r_key, r_value in options_dict['r'].items():
            for n_key, n_value in options_dict['n'].items():
                url = f"{base_url}-{p_value}/{r_value}/{n_value}/"
                urls.append((url, p_value, r_value, n_value))
    return urls


def save_urls_to_db(urls):
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
        CREATE TABLE IF NOT EXISTS urls (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            p_value TEXT NOT NULL,
            r_value TEXT NOT NULL,
            n_value TEXT NOT NULL
        )
    """)

    # Insert URLs into the table
    for url, p_value, r_value, n_value in urls:
        cur.execute("INSERT INTO urls (url, p_value, r_value, n_value) VALUES (%s, %s, %s, %s)",
                    (url, p_value, r_value, n_value))

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    url = 'https://www.nepremicnine.com/'

    # Fetch and parse options
    options_dict = find_all_options(url)

    # Print the tree structure
    print("Tree structure of options:")
    print_tree(options_dict)

    # Generate URLs
    urls = generate_urls(options_dict)

    # Print generated URLs
    print("\nGenerated URLs:")
    for url, p_value, r_value, n_value in urls:
        print(f"{url} (p: {p_value}, r: {r_value}, n: {n_value})")

    # Save URLs to database
    save_urls_to_db(urls)
    logger.info("URLs saved to database successfully.")
