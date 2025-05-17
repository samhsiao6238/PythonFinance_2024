# crawler.py

from bs4 import BeautifulSoup
from urllib.parse import quote
import time
from datetime import datetime

def get_coupang_search_results(driver, search_keyword: str, advanced_keywords: list[str]):
    encoded_keyword = quote(search_keyword)
    url = f"https://www.tw.coupang.com/search?q={encoded_keyword}&channel=user"

    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    product_cards = soup.select("div.SearchResult_searchResultProduct___h6E9")

    now = datetime.now()
    all_results = []
    filtered_results = []

    for card in product_cards:
        try:
            full_text = card.get_text(separator=" ", strip=True)

            title_tag = card.select_one("div.Product_title__8K0xk")
            title = title_tag.get_text(strip=True) if title_tag else "N/A"

            price_tag = card.select_one("span.Product_salePricePrice__2FbsL span")
            price = price_tag.get_text(strip=True) if price_tag else "N/A"

            unit_price_tag = card.select_one("div.Product_unitPrice__QQPdR")
            unit_price = unit_price_tag.get_text(strip=True) if unit_price_tag else "N/A"

            product = {
                "search_keyword": search_keyword,
                "title": title,
                "full_text": full_text,
                "price": price,
                "unit_price": unit_price,
                "timestamp": now
            }

            all_results.append(product)

            if all(kw in full_text for kw in advanced_keywords):
                filtered_results.append(product)

        except Exception as e:
            print("解析錯誤：", e)
            continue

    return all_results, filtered_results
