import requests
from bs4 import BeautifulSoup

URL = 'https://tygia.vn/gia-vang'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())


