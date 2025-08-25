# from .scrappers.gulahmed import gulahmed_scraping 
# from .scrappers.khaadi import khaadi_scraping 
# from .scrappers.minnieminors import minnieminor_scraping 
# from .scrappers.diners import diners_scraping 
# from .scrappers.shoppingum import shoppingum_scraping

# def combined_scraper(query):
#     results = []

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

#     try:
#         results += shoppingum_scraping(query)
#     except Exception as e:
#         print(f"[Diners] Error: {e}")

#     # print("RESULTS: ", results)

#     return results

# # import requests
# # from bs4 import BeautifulSoup
# # from django.utils.http import urlencode
# # from urllib.parse import urljoin
# # import re

# # from .scrappers.gulahmed import gulahmed_scraping 
# # from .scrappers.khaadi import khaadi_scraping 
# # from .scrappers.minnieminors import minnieminor_scraping 
# # from .scrappers.diners import diners_scraping 

# # def combined_scraper(query):
# #     results = []

# #     # try:
# #     #     results += scrap_shoppingum(query)
# #     # except Exception as e:
# #     #     print(f"[ShoppingUM] Error: {e}")

# #     try:
# #         results += gulahmed_scraping(query)
# #     except Exception as e:
# #         print(f"[GulAhmed] Error: {e}")

# #     try:
# #         results += khaadi_scraping(query)
# #     except Exception as e:
# #         print(f"[Khaadi] Error: {e}")

# #     try:
# #         results += minnieminor_scraping(query)
# #     except Exception as e:
# #         print(f"[Minnie Minors] Error: {e}")

# #     try:
# #         results += diners_scraping(query)
# #     except Exception as e:
# #         print(f"[Diners] Error: {e}")

# #     return results


# # # def extract_integer(price_text):
# # #     digits = re.findall(r'\d+', price_text.replace(',', ''))
# # #     return int(''.join(digits)) if digits else None

# # # def scrap_shoppingum(query="black shalwar qameez"):
# # #     base_url = "https://shoppingum.com"
# # #     q_string = urlencode({'search': query})
# # #     url = f"{base_url}/search?{q_string}"

# #     response = requests.get(url, verify=False)  # ignore SSL errors, remove verify=False if certs OK
# #     soup = BeautifulSoup(response.text, 'html.parser')

# #     prod_list = []

# #     # Each product is an <li> with data-card attribute
# #     products = soup.find_all('li', attrs={'data-card': True})

# #     for product in products:
# #         # Image URL from data-src attribute of img.lozad
# #         img_tag = product.find('img', class_='lozad')
# #         img_link = img_tag['data-src'] if img_tag and img_tag.has_attr('data-src') else "N/A"
# #         if img_link != "N/A":
# #             img_link = urljoin(base_url, img_link)

# #         # Product name inside p with class fs-theme-text-purple
# #         name_tag = product.find('p', class_='fs-theme-text-purple')
# #         product_name = name_tag.text.strip() if name_tag else "N/A"

# #         # Prices: old price with line-through and sale price with fs-theme-text-pink-01
# #         price_p = product.find('p', class_='font-bold')
# #         if price_p:
# #             old_price_tag = price_p.find('span', class_='line-through')
# #             sale_price_tag = price_p.find('span', class_=lambda x: x and 'fs-theme-text-pink-01' in x)

# #             regular_price = extract_integer(old_price_tag.text) if old_price_tag else None
# #             sale_price = extract_integer(sale_price_tag.text) if sale_price_tag else regular_price
# #         else:
# #             regular_price = sale_price = None

# #         # Product link from 'Visit Store' anchor tag
# #         visit_store_a = product.find('a', string='Visit Store')
# #         product_link = urljoin(base_url, visit_store_a['href']) if visit_store_a else "N/A"

# #         prod_list.append({
# #             'name': product_name,
# #             'link': product_link,
# #             'image': img_link,
# #             'price': regular_price,
# #             'sale_price': sale_price
# #         })

# #     return prod_list

# # if __name__ == "__main__":
# #     results = scrap_shoppingum("black shalwar qameez")
# #     for product in results:
# #         print(product)
import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from typing import List, Dict, Any
import difflib
import re
 
from .scrappers.gulahmed import gulahmed_scraping
from .scrappers.khaadi import khaadi_scraping
from .scrappers.minnieminors import minnieminor_scraping
from .scrappers.diners import diners_scraping
from .scrappers.shoppingum import shoppingum_scraping
 
def calculate_relevance_score(product_name: str, query: str) -> float:
    """
    Calculate relevance score between product name and search query.
    Returns a score between 0 and 1, where 1 is most relevant.
    """
    if not product_name or not query:
        return 0.0
   
    # Convert to lowercase for case-insensitive comparison
    product_lower = product_name.lower()
    query_lower = query.lower()
   
    # Split query into individual words
    query_words = re.findall(r'\w+', query_lower)
    product_words = re.findall(r'\w+', product_lower)
   
    if not query_words:
        return 0.0
   
    # Calculate different scoring metrics
    scores = []
   
    # 1. Exact phrase match (highest weight)
    if query_lower in product_lower:
        scores.append(1.0)
   
    # 2. Word overlap score
    matched_words = sum(1 for word in query_words if word in product_words)
    word_overlap_score = matched_words / len(query_words)
    scores.append(word_overlap_score * 0.8)
   
    # 3. Fuzzy string similarity using difflib
    similarity_score = difflib.SequenceMatcher(None, query_lower, product_lower).ratio()
    scores.append(similarity_score * 0.6)
   
    # 4. Partial word matches (for variations like "shirt" vs "shirts")
    partial_matches = 0
    for q_word in query_words:
        for p_word in product_words:
            if q_word in p_word or p_word in q_word:
                partial_matches += 1
                break
    partial_score = partial_matches / len(query_words)
    scores.append(partial_score * 0.4)
   
    # Return the maximum score from all methods
    return max(scores) if scores else 0.0
 
def scraper_wrapper(scraper_func, scraper_name: str, query: str) -> Dict[str, Any]:
    """
    Wrapper function to call individual scrapers with error handling and timing.
    """
    start_time = time.time()
    try:
        results = scraper_func(query)
        end_time = time.time()
       
        # Add relevance scores to each product
        for product in results:
            if isinstance(product, dict) and 'name' in product:
                product['relevance_score'] = calculate_relevance_score(product['name'], query)
                product['source'] = scraper_name
       
        return {
            'scraper': scraper_name,
            'results': results,
            'success': True,
            'execution_time': end_time - start_time,
            'error': None
        }
    except Exception as e:
        end_time = time.time()
        print(f"[{scraper_name}] Error: {e}")
        return {
            'scraper': scraper_name,
            'results': [],
            'success': False,
            'execution_time': end_time - start_time,
            'error': str(e)
        }
 
def filter_relevant_results(results: List[Dict], query: str, min_relevance: float = 0.3) -> List[Dict]:
    """
    Filter results based on relevance score and remove duplicates.
    """
    # Filter by minimum relevance score
    relevant_results = [
        product for product in results
        if product.get('relevance_score', 0) >= min_relevance
    ]
   
    # Remove duplicates based on product name similarity
    unique_results = []
    seen_products = set()
   
    for product in relevant_results:
        product_name = product.get('name', '').lower().strip()
       
        # Check if we've seen a very similar product name
        is_duplicate = False
        for seen_name in seen_products:
            if difflib.SequenceMatcher(None, product_name, seen_name).ratio() > 0.85:
                is_duplicate = True
                break
       
        if not is_duplicate and product_name:
            seen_products.add(product_name)
            unique_results.append(product)
   
    return unique_results
 
def combined_scraper(query: str, max_workers: int = 5, timeout: int = 30, min_relevance: float = 0.3) -> List[Dict]:
    """
    Combined scraper using threading for faster execution with query relevance filtering.
   
    Args:
        query: Search query string
        max_workers: Maximum number of threads to use
        timeout: Timeout for each scraper in seconds
        min_relevance: Minimum relevance score to include results (0-1)
   
    Returns:
        List of relevant product dictionaries sorted by relevance score
    """
    if not query or not query.strip():
        return []
   
    # Define scrapers with their functions
    scrapers = [
        (gulahmed_scraping, "GulAhmed"),
        (khaadi_scraping, "Khaadi"),
        (minnieminor_scraping, "Minnie Minors"),
        (diners_scraping, "Diners"),
        (shoppingum_scraping, "ShoppingUM")
    ]
   
    all_results = []
    start_time = time.time()
   
    # Use ThreadPoolExecutor for concurrent execution
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all scraping tasks
        future_to_scraper = {
            executor.submit(scraper_wrapper, scraper_func, scraper_name, query): scraper_name
            for scraper_func, scraper_name in scrapers
        }
       
        # Process completed tasks
        for future in as_completed(future_to_scraper, timeout=timeout):
            scraper_name = future_to_scraper[future]
            try:
                result = future.result()
                if result['success'] and result['results']:
                    all_results.extend(result['results'])
                    print(f"[{scraper_name}] Completed in {result['execution_time']:.2f}s - "
                          f"{len(result['results'])} products found")
                else:
                    print(f"[{scraper_name}] Failed or no results")
            except concurrent.futures.TimeoutError:
                print(f"[{scraper_name}] Timed out after {timeout}s")
            except Exception as e:
                print(f"[{scraper_name}] Unexpected error: {e}")
   
    # Filter results for relevance and remove duplicates
    filtered_results = filter_relevant_results(all_results, query, min_relevance)
   
    # Sort by relevance score (highest first) and then by price if available
    filtered_results.sort(
        key=lambda x: (x.get('relevance_score', 0), -(x.get('price', 0) or 0)),
        reverse=True
    )
   
    total_time = time.time() - start_time
    print(f"Total scraping completed in {total_time:.2f}s - "
          f"{len(filtered_results)} relevant products from {len(all_results)} total")
   
    return filtered_results
 
# Alternative version with more granular control
def combined_scraper_advanced(
    query: str,
    enabled_scrapers: List[str] = None,
    max_workers: int = 5,
    timeout: int = 30,
    min_relevance: float = 0.3,
    max_results: int = 100
) -> Dict[str, Any]:
    """
    Advanced version with more control options and detailed response.
   
    Returns:
        Dictionary with results, metadata, and performance stats
    """
    if not query or not query.strip():
        return {
            'results': [],
            'query': query,
            'total_results': 0,
            'execution_time': 0,
            'scrapers_used': [],
            'errors': []
        }
   
    # All available scrapers
    all_scrapers = {
        'gulahmed': (gulahmed_scraping, "GulAhmed"),
        'khaadi': (khaadi_scraping, "Khaadi"),
        'minnieminors': (minnieminor_scraping, "Minnie Minors"),
        'diners': (diners_scraping, "Diners"),
        'shoppingum': (shoppingum_scraping, "ShoppingUM")
    }
   
    # Filter enabled scrapers
    if enabled_scrapers:
        scrapers = [(func, name) for key, (func, name) in all_scrapers.items()
                   if key in enabled_scrapers]
    else:
        scrapers = list(all_scrapers.values())
   
    all_results = []
    scraper_stats = []
    errors = []
    start_time = time.time()
   
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_scraper = {
            executor.submit(scraper_wrapper, scraper_func, scraper_name, query): scraper_name
            for scraper_func, scraper_name in scrapers
        }
       
        for future in as_completed(future_to_scraper, timeout=timeout):
            scraper_name = future_to_scraper[future]
            try:
                result = future.result()
                scraper_stats.append(result)
               
                if result['success'] and result['results']:
                    all_results.extend(result['results'])
                elif result['error']:
                    errors.append(f"{scraper_name}: {result['error']}")
                   
            except concurrent.futures.TimeoutError:
                errors.append(f"{scraper_name}: Timeout after {timeout}s")
            except Exception as e:
                errors.append(f"{scraper_name}: {str(e)}")
   
    # Filter and sort results
    filtered_results = filter_relevant_results(all_results, query, min_relevance)
   
    # Limit results if specified
    if max_results and len(filtered_results) > max_results:
        filtered_results = filtered_results[:max_results]
   
    total_time = time.time() - start_time
   
    return {
        'results': filtered_results,
        'query': query,
        'total_results': len(filtered_results),
        'raw_results_count': len(all_results),
        'execution_time': total_time,
        'scrapers_used': [stat['scraper'] for stat in scraper_stats if stat['success']],
        'scraper_stats': scraper_stats,
        'errors': errors,
        'filters_applied': {
            'min_relevance': min_relevance,
            'max_results': max_results
        }
    }
 
# Usage example and testing
if __name__ == "__main__":
    # Basic usage
    query = "black shalwar qameez"
    results = combined_scraper(query, max_workers=3, min_relevance=0.2)
   
    print(f"\nFound {len(results)} relevant products for '{query}':")
    for i, product in enumerate(results[:5], 1):  # Show top 5
        print(f"{i}. {product.get('name', 'N/A')} "
              f"(Score: {product.get('relevance_score', 0):.2f}, "
              f"Source: {product.get('source', 'N/A')})")
   
    # Advanced usage
    print("\n" + "="*50)
    advanced_results = combined_scraper_advanced(
        query="women kurta",
        enabled_scrapers=['gulahmed', 'khaadi'],
        max_results=10,
        min_relevance=0.4
    )
   
    print(f"Advanced search completed in {advanced_results['execution_time']:.2f}s")
    print(f"Results: {advanced_results['total_results']} relevant from {advanced_results['raw_results_count']} total")
    if advanced_results['errors']:
        print(f"Errors: {advanced_results['errors']}")