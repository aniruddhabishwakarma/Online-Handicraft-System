import csv
from django.core.management.base import BaseCommand
from recommendation.models import HandicraftProduct
from datetime import datetime

class Command(BaseCommand):
    help = 'Import woolen felt handicraft products from a CSV file into the database'

    def handle(self, *args, **kwargs):
        file_path = "handicrafts.csv"  # CSV should be in project root
        products_to_create = []
        count = 0

        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Skip duplicate entries
                    if HandicraftProduct.objects.filter(url=row['url']).exists():
                        continue

                    try:
                        scraped_time = datetime.strptime(row['scraped_at'], "%Y-%m-%d %H:%M:%S") if row['scraped_at'] else None
                    except Exception:
                        scraped_time = None

                    product = HandicraftProduct(
                        url=row['url'],
                        name=row['name'],
                        price=row['price'] or 0,
                        currency=row['currency'],
                        availability=row['availability'],
                        description=row['description'],
                        category=row['category'],
                        brand=row.get('brand', ''),
                        average_rating=float(row.get('average_rating') or 0.0),
                        reviews_count=int(row.get('reviews_count') or 0),
                        images=row.get('images', ''),
                        product_d=row.get('product_d', ''),
                        scraped_at=scraped_time
                    )

                    products_to_create.append(product)
                    count += 1

            # Fast insert
            HandicraftProduct.objects.bulk_create(products_to_create)
            self.stdout.write(self.style.SUCCESS(f"✅ Imported {count} new products to DB."))

        except FileNotFoundError:
            self.stderr.write("❌ File not found. Make sure 'handicrafts.csv' is in the root directory.")
        except Exception as e:
            self.stderr.write(f"❌ Error occurred: {e}")
