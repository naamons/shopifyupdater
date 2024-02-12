import configparser
import pandas as pd
from web_downloader import download_excel_file, login_to_website
from excel_reader import read_sku_map_from_excel
from shopify_skucheck import compare_and_update_prices
import requests
import csv

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Step 1: Download the Excel file
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    login_to_website(session, config['WebDownloader']['login_url'], {
        'email': config['WebDownloader']['username'],
        'password': config['WebDownloader']['password']
    })
    download_excel_file(session, config['WebDownloader']['download_url'], config['Filepaths']['excel_file_path'])

    # Step 2: Read SKUs and Prices from Excel
    # Read the map_adjustment value from config.ini and convert it to float
    map_adjustment = float(config['Prices']['map_adjustment'])
    # Pass map_adjustment as an argument to the read_sku_map_from_excel function
    sku_price_map = read_sku_map_from_excel(config['Filepaths']['excel_file_path'], map_adjustment)

    # Step 3: Compare and Update Shopify Store
    changes = compare_and_update_prices(config['Shopify']['shop_name'], config['Shopify']['access_token'], sku_price_map)

    # Step 4: Generate CSV Report
    with open(config['Filepaths']['report_file_path'], 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['SKU', 'Old Price', 'New Price'])
        for change in changes:
            writer.writerow(change)

if __name__ == "__main__":
    main()
