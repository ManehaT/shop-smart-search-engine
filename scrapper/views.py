from django.http import JsonResponse
from scrapper.service import combined_scraper
from shop.models import Product  

def search_view(request):
    query = request.GET.get("q")
    if not query:
        return JsonResponse({"error": "Missing 'q' search query."}, status=400)

    try:
        results = combined_scraper(query)
        print("Resultas: ", results)


        # Save scraped products to DB
        for item in results:
            # print(f"Scraped brand: {item.get('brand')}")  # debug print brands
            print(f"Scraped brand: {item.get('brand')}")  # debug print brands
            
            print("About to insert product with values:")
            print(f"name: {item['name']}")
            print(f"brand: {item.get('brand', 'Test')}")
            print(f"product_url: {item['link']}")
            print(f"image_url: {item['image']}")
            print(f"price: {item['price']}")
            print(f"sale_price: {item['sale_price']}")
            print(f"created_by: {request.user if request.user.is_authenticated else ''}")
            print("-----")

            if not Product.objects.filter(product_url=item['link']).exists():
                print("HERE")
                Product.objects.get_or_create(
                    product_url=item['link'],
                    defaults={
                        'category': "category",
                        'brand': item.get("brand", "Test"),
                        'created_by': request.user if request.user.is_authenticated else "",
                        'name': item['name'],
                        'image_url': item['image'],
                        'price': item['price'],
                        'sale_price': item['sale_price'],
                    }
                )
                print("HERE")

        return JsonResponse({"results": results}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
