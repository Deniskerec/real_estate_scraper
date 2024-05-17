import requests
import logging
from bs4 import BeautifulSoup
import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_all_options(url, headers):
    response = requests.get(url, headers=headers)

    options_dict = {
        'p': {},
        'n': {},
        'r': {}
    }

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Options for 'p'
        select_element = soup.find('select', {'name': 'p'})
        if select_element:
            options = select_element.find_all('option')
            for option in options:
                value = option.get('value')
                text = replace_special_characters(option.text.lower())
                options_dict['p'][value] = text

        # Options for 'n'
        select_element = soup.find('select', {'name': 'n'})
        if select_element:
            options = select_element.find_all('option')
            for option in options:
                value = option.get('value')
                text = replace_special_characters(option.text.lower())
                options_dict['n'][value] = text

        # Hardcoded options for 'r'
        options_dict['r'] = {
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
        cur.execute("INSERT INTO urls (url, p_value, r_value, n_value) VALUES (%s, %s, %s, %s)", (url, p_value, r_value, n_value))

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    url = 'https://nepremicnine.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Fetch and parse options
    options_dict = find_all_options(url, headers)

    # Print the tree structure
    print("Tree structure of options:")
    print_tree(options_dict)

    # # Generate URLs
    # urls = generate_urls(options_dict)
    #
    # # Print generated URLs
    # print("\nGenerated URLs:")
    # for url, p_value, r_value, n_value in urls:
    #     print(f"{url} (p: {p_value}, r: {r_value}, n: {n_value})")
    #
    # # Save URLs to database
    # save_urls_to_db(urls)
