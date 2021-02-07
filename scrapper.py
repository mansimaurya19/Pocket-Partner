import requests
from bs4 import BeautifulSoup
import smtplib
import re
import json

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}


# to extract only the necessary part of the product's url
def extract_url(url):
    index = url.find("B0")
    index = index + 10
    current_url = ""
    current_url = url[:index]
    # print(current_url)
    return current_url


# function to scrap product details
def get_product_details(url):
    url = extract_url(url)
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # product's name
    title = soup.find(id="productTitle").get_text().strip()
    # product's price
    price = soup.find(id="priceblock_dealprice")
    # print(price)
    if price == None:
        price = soup.find(id="priceblock_ourprice")
        # print(price)
    if price == None:
        price = soup.find(id="priceblock_salesprice")
    # product's availability
    availability = soup.find(id="availability")
    if availability == None:
        availability = "N/A"
    else:
        availability = availability.get_text().strip()[:-1]
    # product's image
    img_div = soup.find(id="imgTagWrapperId")
    # a string in Json format
    imgs_str = img_div.img.get('data-a-dynamic-image')
    # convert to a dictionary
    imgs_dict = json.loads(imgs_str)
    # each key in the dictionary is a link of an image, and the value shows the size (print all the dictionay to inspect)
    num_element = 0
    first_link = list(imgs_dict.keys())[num_element]
    image = first_link

    converted_price = float(re.sub(r"[^\d.]", "", price.get_text()))

    details = {"name": title, "price": converted_price, "url": url,
               "availability": availability, "image_url": image}
    return details
