from django.db import models
from django.conf import settings

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
    
class Question(models.Model):
    STATUS_CHOICES = (
        ('UNANSWERED', 'Unanswered'),
        ('ANSWERED', 'Answered'),
    )

    product = models.ForeignKey('HandicraftProduct', on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UNANSWERED')

    def __str__(self):
        return f"Q: {self.content[:30]}..."

class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='answer')
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"A to: {self.question.content[:30]}..."
