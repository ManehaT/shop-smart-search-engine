def khaadi_scraping(query=""):
    import requests
    from bs4 import BeautifulSoup
    import re
    from django.utils.http import urlencode

    q = urlencode({"q": query})
    url = f"https://pk.khaadi.com/catalogsearch/result/?{q}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', class_='product-tile')

    prod_json = []

    def extract_integer(price_text):
        digits = re.findall(r'\d+', price_text.replace(',', ''))
        return int(''.join(digits)) if digits else None

    for product in products:
        try:
            product_link = "https://pk.khaadi.com" + product.find('a', class_='link plpRedirectPdp')['href']
            product_name = product.find('a', class_='link').text.strip()
        except Exception:
            continue

        img_tag = product.find('img', class_='tile-image')
        img_link = img_tag['src'] if img_tag else "N/A"

        price_container = product.find('div', class_='price')
        regular_price = sale_price = None

        if price_container:
            old_price = price_container.find('span', class_='old-price')
            special_price = price_container.find('span', class_='special-price')
            current_price = price_container.find('span', class_='value')

            if old_price and special_price:
                regular_price = extract_integer(old_price.text)
                sale_price = extract_integer(special_price.text)
            elif current_price:
                price = extract_integer(current_price.text)
                regular_price = sale_price = price

        prod_json.append({
            'name': product_name,
            'link': product_link,
            'image': img_link,
            'price': regular_price,
            'sale_price': sale_price,
        })

    return prod_json
