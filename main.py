from bs4 import BeautifulSoup
import requests


def scrape_product(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')

    catalog_container = soup.find('div', class_='usedProductNext')

    product_items = catalog_container.find_all('div', class_='itemTitle')
    product_prices = catalog_container.find_all('span', class_='price contractPrice')

    if len(product_items) == len(product_prices):
        for name, price in zip(product_items, product_prices):
            yield name.text.strip(), price.text.strip()
    else:
        print("Количество названий и цен не совпадает.")


# url = 'https://autoliga.net.ua/catalog/volkswagen/-tiguan-ii-15-17/1/'
# url = 'https://autoliga.net.ua/catalog/porsche/-cayenne-18--9y/1/'
# url = 'https://autoliga.net.ua/catalog/toyota/-camry-v70-18-/1/'
# for name, price in scrape_product(url):
#     print(name, '-', price)


# script start scrape every day at 08:00





