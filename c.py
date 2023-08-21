import requests
from bs4 import BeautifulSoup
import time
import csv

# Create a list to store the scraped data
data = []

# Loop through the first 20 pages of the product listing pages
for i in range(1, 21):
    # Send a GET request to the page URL and get the HTML content
    url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{i}"
    response = requests.get(url)
    content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Find all the product containers on the page
    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    # Loop through each product container and extract the required information
    for product in products:
        # Extract product URL
        url = "https://www.amazon.in" + \
            product.find("a", {"class": "a-link-normal"})["href"]

        # Extract product name
        name = product.find("span", {"class": "a-size-medium"}).text.strip()

        # Extract product price
        price = product.find("span", {"class": "a-price-whole"}).text.strip()

        # Extract product rating
        rating = product.find("span", {"class": "a-icon-alt"}).text.strip()

        # Extract number of reviews
        reviews = product.find("span", {"class": "a-size-base"}).text.strip()

        # Append the extracted information to the list
        data.append([url, name, price, rating, reviews])

    # Wait for a few seconds before sending the next request
    time.sleep(5)

# Save the data to a CSV file
with open("amazon_products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Name", "Price", "Rating", "Reviews"])
    writer.writerows(data)
