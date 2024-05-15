import logging
import os
from scrapers.nepremicnine_scraper import nepremine_net_access_test

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

def run_nepremicnine_test():
    content = nepremine_net_access_test()
    if content:
        print("Connection successful, content retrieved.")
    else:
        print("Failed to retrieve content.")

# def run_random_test():
#     result = random_test()
#     print(result)

if __name__ == "__main__":
    # Test nepremicnine_net_access_test
    run_nepremicnine_test()
    # Uncomment to test random_test
    # run_random_test()
