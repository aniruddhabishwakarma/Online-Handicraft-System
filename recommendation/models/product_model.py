from django.db import models

class HandicraftProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="NPR")
    description = models.TextField()
    image_file = models.ImageField(upload_to='products/', blank=True, null=True) 
    quantity_available = models.PositiveIntegerField(default=1)
    
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products', default=1)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
