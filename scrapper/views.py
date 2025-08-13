from django.http import JsonResponse
from scrapper.service import combined_scraper
from shop.models import Product  

def search_view(request):
    query = request.GET.get("q")
    if not query:
        return JsonResponse({"error": "Missing 'q' search query."}, status=400)

    try:
        results = combined_scraper(query)
        print("Results: ", results)

        # Save scraped products to DB
        for item in results:
            # Sanitize values
            brand = item.get('brand') if item.get('brand') else 'Test'
            price = item.get('price') if item.get('price') is not None else 0
            sale_price = item.get('sale_price') if item.get('sale_price') is not None else 0

            print("About to insert product with values:")
            print(f"name: {item['name']}")
            print(f"brand: {brand}")
            print(f"product_url: {item['link']}")
            print(f"image_url: {item['image']}")
            print(f"price: {price}")
            print(f"sale_price: {sale_price}")
            print(f"created_by: {request.user if request.user.is_authenticated else ''}")
            print("-----")

            # Insert if product does not already exist
            if not Product.objects.filter(product_url=item['link']).exists():
                Product.objects.get_or_create(
                    product_url=item['link'],
                    defaults={
                        'category': "category",
                        'brand': brand,
                        'created_by': request.user if request.user.is_authenticated else "",
                        'name': item['name'],
                        'image_url': item['image'],
                        'price': price,
                        'sale_price': sale_price,
                    }
                )

        return JsonResponse({"results": results}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
