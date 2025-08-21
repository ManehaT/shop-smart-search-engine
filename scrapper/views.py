from django.http import JsonResponse
from scrapper.service import combined_scraper
from shop.models import Product  

def search_view(request):
    query = request.GET.get("q")
    if not query:
        return JsonResponse({"error": "Missing 'q' search query."}, status=400)

    try:
        results = combined_scraper(query)


        # Save scraped products to DB
        for item in results:
            if not Product.objects.filter(product_url=item['link']).exists():
                Product.objects.get_or_create(
                    product_url=item['link'],
                    defaults={
                        'category': "Test",
                        'brand': "My Shop",
                        'created_by': request.user if request.user.is_authenticated else "",
                        'name': item['name'],
                        'image_url': item['image'],
                        'price': item['price'],
                        'sale_price': item['sale_price'],
                    }
                )

        return JsonResponse({"results": results}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
