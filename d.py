import requests
from bs4 import BeautifulSoup
import csv

# Read the product URLs from the CSV file
with open("amazon_products.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # skip the header row
    urls = [row[0] for row in reader]

# Create a list to store the scraped data
data = []

# Loop through each product URL
for url in urls:
    # Send a GET request to the product URL and get the HTML content
    response = requests.get(url)
    content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Extract the required information
    try:
        description = soup.find("span", {"id": "productTitle"}).text.strip()
    except:
        description = ""

    try:
        asin = soup.find("th", {"class": "prodDetSectionEntry"}).text.strip()
    except:
        asin = ""

    try:
        product_description = soup.find(
            "div", {"id": "productDescription"}).text.strip()
    except:
        product_description = ""

    try:
        manufacturer = soup.find("a", {"id": "bylineInfo"}).text.strip()
    except:
        manufacturer = ""

    # Append the extracted information to the list
    data.append([url, description, asin, product_description, manufacturer])

# Save the data to a new CSV file
with open("amazon_product_details.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Description", "ASIN",
                    "Product Description", "Manufacturer"])
    writer.writerows(data)
