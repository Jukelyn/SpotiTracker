import sys

# For webscraping
from bs4 import BeautifulSoup

# For accessing websites
import requests

# url = "https://songstats.com/artist/bxvi8c2k/juhye"
url = "https://webscraper.io/test-sites/e-commerce/allinone/product/29"

try:
    result = requests.get(url)
    # print(result.status_code)
except requests.ConnectionError:
    print("Failed to connect")

page = BeautifulSoup(result.text, "html.parser")

# print(page.prettify())

current_monthly_listeners = page.find_all("Android")
print(current_monthly_listeners)