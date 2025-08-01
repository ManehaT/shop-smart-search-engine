def minnieminor_scraping(query=""):
    import requests

    # For now, defaulting to one collection; ShoppingUM-style query matching not supported
    url = "https://www.minnieminors.com/collections/baby-girls-western/products.json"
    response = requests.get(url)
    data = response.json()

    prod_list = []

    def to_int(value):
        try:
            return int(float(value))
        except:
            return None

    for product in data.get('products', []):
        product_name = product['title']
        product_link = f"https://www.minnieminors.com/products/{product['handle']}"
        image = product['images'][0]['src'] if product.get('images') else "N/A"

        regular_price = sale_price = None

        if product.get('variants'):
            variant = product['variants'][0]
            price = to_int(variant.get('price', 0))
            compare_at = to_int(variant.get('compare_at_price'))

            if compare_at and compare_at > price:
                regular_price = compare_at
                sale_price = price
            else:
                regular_price = sale_price = price

        prod_list.append({
            'name': product_name,
            'link': product_link,
            'image': image,
            'price': regular_price,
            'sale_price': sale_price
        })

    return prod_list
