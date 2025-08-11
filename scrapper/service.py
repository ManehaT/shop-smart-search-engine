from .scrappers.gulahmed import gulahmed_scraping 
from .scrappers.khaadi import khaadi_scraping 
from .scrappers.minnieminors import minnieminor_scraping 
from .scrappers.diners import diners_scraping 
from .scrappers.shoppingum import shoppingum_scraping

def combined_scraper(query):
    results = []

    try:
        results += gulahmed_scraping(query)
    except Exception as e:
        print(f"[GulAhmed] Error: {e}")

    try:
        results += khaadi_scraping(query)
    except Exception as e:
        print(f"[Khaadi] Error: {e}")

    try:
        results += minnieminor_scraping(query)
    except Exception as e:
        print(f"[Minnie Minors] Error: {e}")

    try:
        results += diners_scraping(query)
    except Exception as e:
        print(f"[Diners] Error: {e}")

    try:
        results += shoppingum_scraping(query)
    except Exception as e:
        print(f"[Diners] Error: {e}")

    return results

# import requests
# from bs4 import BeautifulSoup
# from django.utils.http import urlencode
# from urllib.parse import urljoin
# import re

# from .scrappers.gulahmed import gulahmed_scraping 
# from .scrappers.khaadi import khaadi_scraping 
# from .scrappers.minnieminors import minnieminor_scraping 
# from .scrappers.diners import diners_scraping 

# def combined_scraper(query):
#     results = []

#     # try:
#     #     results += scrap_shoppingum(query)
#     # except Exception as e:
#     #     print(f"[ShoppingUM] Error: {e}")

#     try:
#         results += gulahmed_scraping(query)
#     except Exception as e:
#         print(f"[GulAhmed] Error: {e}")

#     try:
#         results += khaadi_scraping(query)
#     except Exception as e:
#         print(f"[Khaadi] Error: {e}")

#     try:
#         results += minnieminor_scraping(query)
#     except Exception as e:
#         print(f"[Minnie Minors] Error: {e}")

#     try:
#         results += diners_scraping(query)
#     except Exception as e:
#         print(f"[Diners] Error: {e}")

#     return results


# # def extract_integer(price_text):
# #     digits = re.findall(r'\d+', price_text.replace(',', ''))
# #     return int(''.join(digits)) if digits else None

# # def scrap_shoppingum(query="black shalwar qameez"):
# #     base_url = "https://shoppingum.com"
# #     q_string = urlencode({'search': query})
# #     url = f"{base_url}/search?{q_string}"

#     response = requests.get(url, verify=False)  # ignore SSL errors, remove verify=False if certs OK
#     soup = BeautifulSoup(response.text, 'html.parser')

#     prod_list = []

#     # Each product is an <li> with data-card attribute
#     products = soup.find_all('li', attrs={'data-card': True})

#     for product in products:
#         # Image URL from data-src attribute of img.lozad
#         img_tag = product.find('img', class_='lozad')
#         img_link = img_tag['data-src'] if img_tag and img_tag.has_attr('data-src') else "N/A"
#         if img_link != "N/A":
#             img_link = urljoin(base_url, img_link)

#         # Product name inside p with class fs-theme-text-purple
#         name_tag = product.find('p', class_='fs-theme-text-purple')
#         product_name = name_tag.text.strip() if name_tag else "N/A"

#         # Prices: old price with line-through and sale price with fs-theme-text-pink-01
#         price_p = product.find('p', class_='font-bold')
#         if price_p:
#             old_price_tag = price_p.find('span', class_='line-through')
#             sale_price_tag = price_p.find('span', class_=lambda x: x and 'fs-theme-text-pink-01' in x)

#             regular_price = extract_integer(old_price_tag.text) if old_price_tag else None
#             sale_price = extract_integer(sale_price_tag.text) if sale_price_tag else regular_price
#         else:
#             regular_price = sale_price = None

#         # Product link from 'Visit Store' anchor tag
#         visit_store_a = product.find('a', string='Visit Store')
#         product_link = urljoin(base_url, visit_store_a['href']) if visit_store_a else "N/A"

#         prod_list.append({
#             'name': product_name,
#             'link': product_link,
#             'image': img_link,
#             'price': regular_price,
#             'sale_price': sale_price
#         })

#     return prod_list

# if __name__ == "__main__":
#     results = scrap_shoppingum("black shalwar qameez")
#     for product in results:
#         print(product)
