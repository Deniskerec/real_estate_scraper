import requests
import logging

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


nepremine_net_access_test()



