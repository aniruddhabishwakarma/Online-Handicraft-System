from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


class Command(BaseCommand):
    help = 'Scrape wool felt dolls from eBay and save to CSV'

    def handle(self, *args, **kwargs):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        base_url = "https://www.ebay.com/sch/i.html?_nkw=wool+felt+doll&_pgn={page}"
        products = []

        for page in range(1, 10):
            self.stdout.write(f"📄 Scraping page {page}")
            url = base_url.format(page=page)
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")

            items = soup.select(".s-item")

            for item in items:
                title_tag = item.select_one(".s-item__title")
                price_tag = item.select_one(".s-item__price")
                image_tag = item.select_one(".s-item__image-img")
                link_tag = item.select_one(".s-item__link")

                if not title_tag or not price_tag or not image_tag:
                    continue

                title = title_tag.text.strip()
                price_text = price_tag.text.strip().replace("$", "").split()[0]

                try:
                    price = float(price_text.replace(",", ""))
                except:
                    price = round(random.uniform(10, 30), 2)

                image_url = image_tag.get("src") or image_tag.get("data-src")
                product_url = link_tag["href"].split("?")[0] if link_tag else ""

                product = {
                    "title": title,
                    "price": price,
                    "short_description": f"Handmade {random.choice(['soft', 'mini', 'woolen', 'adorable'])} felt doll.",
                    "full_description": f"{title} is a beautiful wool felt doll perfect for collectors or gift lovers. Crafted with care.",
                    "category": "Felt Dolls",
                    "image_url": image_url,
                    "product_url": product_url
                }

                products.append(product)

            time.sleep(1.5)

        df = pd.DataFrame(products)
        df.to_csv("ebay_felt_dolls.csv", index=False)
        self.stdout.write(self.style.SUCCESS(f"✅ Saved {len(products)} products to ebay_felt_dolls.csv"))
