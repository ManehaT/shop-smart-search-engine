def diners_scraping(query=""):
    import requests

    # NOTE: Diners doesn't support search via JSON, so query is ignored for now
    url = "https://diners.com.pk/collections/casual-classic-shirts/products.json"
    response = requests.get(url)
    data = response.json()

    prod_json = []

    for product in data['products']:
        product_name = product['title']
        product_link = f"https://diners.com.pk/products/{product['handle']}"
        
        image = product['images'][0]['src'] if product['images'] else "N/A"
        
        variant = product['variants'][0] if product['variants'] else None

        if variant:
            raw_price = variant['price']
            raw_compare_at_price = variant['compare_at_price']

            if raw_compare_at_price and float(raw_compare_at_price) > float(raw_price):
                regular_price = int(float(raw_compare_at_price))
                sale_price = int(float(raw_price))
            else:
                price = int(float(raw_price))
                regular_price = sale_price = price
        else:
            regular_price = sale_price = None

        prod_json.append({
            'name': product_name,
            'link': product_link,
            'image': image,
            'price': regular_price,
            'sale_price': sale_price
        })

    return prod_json
