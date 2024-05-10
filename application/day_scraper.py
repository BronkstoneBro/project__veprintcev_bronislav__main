import schedule
import time
from application.scrape_product.autoliga import scrape_product


def start_scrape():
    urls = [
        'https://autoliga.net.ua/catalog/volkswagen/-tiguan-ii-15-17/1/',
        'https://autoliga.net.ua/catalog/porsche/-cayenne-18--9y/1/',
        'https://autoliga.net.ua/catalog/toyota/-camry-v70-18-/1/'
    ]
    for url in urls:
        print("Parsing products from", url)
        scrape_product(url)
        print("Parsing complete.")


schedule.every().day.at("08:00").do(start_scrape)

while True:
    schedule.run_pending()
    time.sleep(60)

# script start scrape every day at 08:00