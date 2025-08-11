# from bs4 import BeautifulSoup,SoupStrainer
# import requests
# import sys
# import re
 
 
# base_url = "https://fashionista.shoppingum.com"
# q_string = "search=blue+shirt"
# link = f"{base_url}/search?search={q_string}"
# req = requests.get(link, verify=False)
# soup = BeautifulSoup(req.text, 'lxml')
 
# print(link)
 
 
# def clean_and_sentence_case(text: str) -> str:
#     # Remove leading/trailing spaces and convert to lowercase
#     cleaned = text.strip().lower()
 
#     # Optionally replace multiple spaces with single space
#     cleaned = ' '.join(cleaned.split())
 
#     # Capitalize the first character
#     return cleaned.capitalize()
 
 
 
 
# products = soup.find_all('li',{'class':'outline-none flex flex-col'})
 
 
# for key,product in enumerate(products):
 
 
#         link  = product.find('a').get('href')
 
#         image = base_url + product.find('img').get('data-src')
 
#         item_link = base_url + product.find('a', rel='nofollow', string=re.compile(r'visit store', re.I)).get('href')
 
 
       
#         title = product.find('p', {'class': 'mt-1 mb-1 overflow-hidden text-sm l-line-clamp-2 fs-theme-text-purple md:text-lg'}).text
#         title = clean_and_sentence_case(title)
       
#         brand_name = product.find('p', {'class': 'text-xs leading-3 md:text-sm'}).text
#         brand_name = clean_and_sentence_case(brand_name)
 
#         prices = product.find('p', {'class': 'font-bold md:text-xl'}).find_all('span')
 
#         if len(prices) == 1:
#             price = float(prices[0].get_text().replace('Rs.', '').replace(',', '').strip())
#             regular_price = sale_price = price
#         elif len(prices) >= 2:
#             price_values = [
#                 float(p.get_text().replace('Rs.', '').replace(',', '').strip())
#                 for p in prices
#             ]
#             regular_price = max(price_values)
#             sale_price = min(price_values)
#         else:
#             regular_price = sale_price = None
 
 
#         print('Title : ',title)
#         print('Brand Name : ',brand_name)
#         print('Sale Price : ',sale_price)
#         print('Regular Price : ',regular_price)
#         print('Image Link : ',image)
#         print('Item Link : ',item_link)

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def shoppingum_scraping(query=""):
    base_url = "https://fashionista.shoppingum.com"
    q_string = urlencode({'search': query})
    url = f"{base_url}/search?{q_string}"

    try:
        response = requests.get(url, verify=False)  # Set verify=True in production
        soup = BeautifulSoup(response.text, 'lxml')
    except Exception as e:
        print(f"[ShoppingUM] Request Error: {e}")
        return []

    products = soup.find_all('li', {'class': 'outline-none flex flex-col'})
    prod_list = []

    def clean_and_sentence_case(text: str) -> str:
        cleaned = text.strip().lower()
        cleaned = ' '.join(cleaned.split())
        return cleaned.capitalize()

    def extract_price(text):
        try:
            return float(text.replace('Rs.', '').replace(',', '').strip())
        except:
            return None

    for product in products:
        try:
            title_tag = product.find('p', {'class': 'mt-1 mb-1 overflow-hidden text-sm l-line-clamp-2 fs-theme-text-purple md:text-lg'})
            brand_tag = product.find('p', {'class': 'text-xs leading-3 md:text-sm'})
            price_tags = product.find('p', {'class': 'font-bold md:text-xl'}).find_all('span')
            img_tag = product.find('img')
            visit_link_tag = product.find('a', rel='nofollow', string=re.compile(r'visit store', re.I))

            title = clean_and_sentence_case(title_tag.text) if title_tag else "N/A"
            brand_name = clean_and_sentence_case(brand_tag.text) if brand_tag else "N/A"

            if len(price_tags) == 1:
                price = extract_price(price_tags[0].text)
                regular_price = sale_price = price
            elif len(price_tags) >= 2:
                prices = [extract_price(p.text) for p in price_tags]
                regular_price = max(prices)
                sale_price = min(prices)
            else:
                regular_price = sale_price = None

            image = base_url + img_tag['data-src'] if img_tag else "N/A"
            item_link = base_url + visit_link_tag['href'] if visit_link_tag else "N/A"

            prod_list.append({
                'name': title,
                'brand': brand_name,
                'link': item_link,
                'image': image,
                'price': regular_price,
                'sale_price': sale_price
            })

        except Exception as e:
            print(f"[ShoppingUM] Parsing Error: {e}")
            continue

    return prod_list
