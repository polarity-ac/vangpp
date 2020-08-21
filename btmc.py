import requests
from bs4 import BeautifulSoup

URL = 'https://tygia.vn/gia-vang/bao-tin-minh-chau'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
full_vang = soup.find(id = 'GoldPriceDetail')
vang = full_vang.find_all('span', class_='text-green font-weight-bold')