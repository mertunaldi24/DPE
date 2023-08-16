import csv
import requests
from bs4 import BeautifulSoup


# Read CSV file
with open('Products_Liquisto_Published.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        vendor = row['Vendor']
        barcode = row['Barcode (ISBN, UPC, GTIN, etc.)']
        
        # Combine vendor and barcode to create search query
        search_query = f"{vendor} {barcode}"
        
        # Construct URL and send request
        search_url = f"https://de.wiaautomation.com/q={search_query}"
        response = requests.get(search_url)
        html_content = response.text
        
        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check if product found in search results
        not_found_element = soup.find('div', class_='not-found-message')
        if not_found_element:
            print(f"Product: {vendor} - {barcode} not found")
            continue
        
        # Extract price information based on HTML structure
        price_element = soup.find('span', class_='price')
        if price_element:
            price = price_element.text
            print(f"Product: {vendor} - {barcode}, Price: {price}")
        else:
            print(f"Price not found for {vendor} - {barcode}")
