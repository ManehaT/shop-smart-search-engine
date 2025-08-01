def gulahmed_scraping(query=""):
    import requests
    from bs4 import BeautifulSoup
    import re

    url = f"https://www.gulahmedshop.com/catalogsearch/result/?q={query}"
    # url = "https://www.gulahmedshop.com/mens-clothes"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('li', class_='item product product-item')
    prod_json = []
    def extract_integer(price_text):
        digits = re.findall(r'\d+', price_text.replace(',', ''))
        return int(''.join(digits)) if digits else None

    for product in products:
        # product link and name
        link_tag = product.find('a', class_='product photo product-item-photo')
        product_link = link_tag['href'] if link_tag else "N/A"
        product_name = product_link.split('/')[-1].replace('-', ' ').upper() if product_link != "N/A" else "N/A"
        # product image
        img_tag = product.find('img', class_='product-image-photo')
        img_link = img_tag['src'] if img_tag else "N/A"
        # product price 
        price_container = product.find('div', class_='price-box')
        # regular_price = "N/A"
        # sale_price = "N/A"
        regular_price = None
        sale_price = None

        if price_container:
            old_price_tag = price_container.find('span', class_='old-price')
            special_price_tag = price_container.find('span', class_='special-price')
            current_price_tag = price_container.find('span', class_='price')
            if old_price_tag and special_price_tag:
                regular_price = extract_integer(old_price_tag.text)
                sale_price = extract_integer(special_price_tag.text)
            elif current_price_tag:
                # same price for both
                price = extract_integer(current_price_tag.text)
                regular_price = price
                sale_price = price
        # print("Product Name:", product_name)
        # print("Product Link:", product_link)
        # print("Image Link:", img_link)
        # print("Regular Price:", regular_price)
        # print("Sale Price:", sale_price)
        # print("-" * 60)
        
        obj1 = {
            'name' : product_name,
            'link' : product_link,
            'image' : img_link,
            'price': regular_price,
            'sale_price' : sale_price,
        }

        prod_json.append(obj1)


    return prod_json

gulahmed_scraping()