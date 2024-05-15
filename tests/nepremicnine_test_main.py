import logging
import os
from nepremicnine_tests_definition import nepremine_net_access_test, get_urls_from_db, check_urls

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(
    filename='logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def run_nepremicnine_access_test():
    content = nepremine_net_access_test()
    if content:
        print("Connection successful, content retrieved.")
    else:
        print("Failed to retrieve content.")

# def check_urls_nepremicnine(urls):
#     if urls:
#         check_urls(urls)
#     else:
#         print("No URLs retrieved.")

if __name__ == "__main__":
    run_nepremicnine_access_test()
    # urls = get_urls_from_db()
    # check_urls_nepremicnine(urls)
