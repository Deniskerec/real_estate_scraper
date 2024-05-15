from wsgiref import headers

import requests
import logging
import psycopg2

logger = logging.getLogger(__name__)

def nepremine_net_access_test():
    url = 'https://www.nepremicnine.net/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            logger.info("Successfully connected to the website.")
            return response.content
        else:
            logger.error(f"Failed to retrieve the web page. Status code: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None

# def get_urls_from_db():
#     # Database connection parameters
#     conn_params = {
#         'dbname': 'real_estate',
#         'user': 'postgres',
#         'password': 'postgres',
#         'host': 'localhost'
#     }
#
#     # Connect to the database
#     conn = psycopg2.connect(**conn_params)
#     cur = conn.cursor()
#
#     # Fetch URLs from the database
#     cur.execute("SELECT url FROM urls")
#     urls = [row[0] for row in cur.fetchall()]
#     #print(urls)
#
#     # Close the connection
#     cur.close()
#     conn.close()
#
#     return urls
#
# def check_urls(urls):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }
#     for url in urls:
#         try:
#             response = requests.get(url, headers=headers)
#             if response.status_code == 200:
#                 logger.info(f"URL {url} returned status code 200")
#             else:
#                 logger.error(f"URL {url} returned status code {response.status_code}")
#         except requests.RequestException as e:
#             logger.error(f"Failed to fetch URL {url}: {e}")
