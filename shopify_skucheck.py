
import requests
import configparser
import pandas as pd
from itertools import islice
import math

def get_price_by_sku(shop_name, access_token, sku):
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }
    products_url = f"https://{shop_name}.myshopify.com/admin/api/2022-04/products.json?limit=250"  # Use the maximum limit to reduce the number of pages

    while products_url:
        response = requests.get(products_url, headers=headers)
        if response.status_code == 200:
            products = response.json().get('products', [])
            for product in products:
                for variant in product.get('variants', []):
                    if variant.get('sku') == sku:
                        return variant.get('price'), variant.get('id')

            # Improved Pagination: Extract the URL for the next page of products
            link_header = response.headers.get('Link', None)
            next_link = None
            if link_header:
                links = link_header.split(',')
                for link in links:
                    if 'rel="next"' in link:
                        next_link = link.split(';')[0].strip().strip('<>').strip()
                        break
            products_url = next_link  # Update the URL for the next iteration
        else:
            print(f"Failed to fetch products, status code: {response.status_code}")
            break  # Exit the loop if there's an error

    return None, None  # Return None if the SKU is not found after searching all pages

def update_price(shop_name, access_token, variant_id, new_price):
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }
    update_url = f"https://{shop_name}.myshopify.com/admin/api/2022-04/variants/{variant_id}.json"
    data = {
        "variant": {
            "id": variant_id,
            "price": new_price
        }
    }
    response = requests.put(update_url, json=data, headers=headers)
    if not response.ok:
        print(f"Failed to update price for variant ID {variant_id}, status code: {response.status_code}")
    return response.ok

def compare_and_update_prices(shop_name, access_token, sku_price_map):
    changes = []  # Initialize an empty list to store changes
    # change = {'sku': 'sku', 'old_price': 'current_price', 'new_price': 'expected_price', 'update_success': '1'}
    
    # for sku, expected_price in islice(sku_price_map.items(), 20):
    for sku, expected_price in sku_price_map.items():
        current_price, variant_id = get_price_by_sku(shop_name, access_token, sku)
        
        if current_price:
            current_price = math.ceil(float(current_price)*100)/100
            expected_price = math.ceil(float(expected_price)*100)/100
        
            if current_price != expected_price:
                update_success = update_price(shop_name, access_token, variant_id, expected_price)
                change = {'sku': sku, 'old_price': current_price, 'new_price': expected_price, 'update_success': update_success}
                changes.append(change)  # Append the change to the list if the price was updated successfully or not
                if update_success:
                    print(f"Updated SKU {sku} price from {current_price} to {expected_price}")
                else:
                    print(f"Failed to update SKU {sku}")
        # change = {'sku': 'sku', 'old_price': 'current_price', 'new_price': 'expected_price', 'update_success': '1'}
        # for i in range(4):
        #     changes.append(change.copy())
       
        
    return changes  # Return the list of changes

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    shop_name = config['Shopify']['shop_name']
    access_token = config['Shopify']['access_token']
    file_path = config['Filepaths']['excel_file_path']

    # Read SKU and prices from Excel
    df = pd.read_excel(file_path)
    sku_price_map = dict(zip(df['Article code'], df['Price, USD']))

    changes = compare_and_update_prices(shop_name, access_token, sku_price_map)
    for change in changes:
        print("second")
        print(change)  # Print each change
