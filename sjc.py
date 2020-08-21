import requests
from bs4 import BeautifulSoup

# will be back when we learn global var and import

URL = 'https://tygia.vn/gia-vang'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())
sauce = list(soup.find('tbody').find_all('tr'))

metadata = dict({
    gold.find('th').contents[0].strip('\n\r '): {
    "buy":gold.find('span', class_='text-green font-weight-bold').contents[0],
    "sell":gold.find('span', class_='text-red font-weight-bold').contents[0]
    } for gold in sauce[8:23]
})

metadata["Hồ Chí Minh"] = {
    "buy":sauce[0].find('span', class_='text-green font-weight-bold').contents[0], 
    "sell":sauce[0].find('span', class_='text-red font-weight-bold').contents[0]
}

def update_sjc():
    URL = 'https://tygia.vn/gia-vang'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    sauce = list(soup.find('tbody').find_all('tr'))
    metadata = dict({
        gold.find('th').contents[0].strip('\n\r '): {
            "buy":gold.find('span', class_='text-green font-weight-bold').contents[0],
            "sell":gold.find('span', class_='text-red font-weight-bold').contents[0]
        } for gold in sauce[8:23]
    })
    metadata["Hồ Chí Minh"] = {
        "buy":sauce[0].find('span', class_='text-green font-weight-bold').contents[0], 
        "sell":sauce[0].find('span', class_='text-red font-weight-bold').contents[0]
    }
    return "data updated"

def ask_sjc(city):
    city = city.strip(" ")
    if city in metadata:
        return "giá sjc mua của " + city + " là " + metadata[city]["buy"] + "VND, bán là " + metadata[city]["sell"] + 'VND'
    else:
        return city + " không có hoặc hãy kiểm tra dấu và viết hoa"