from django.db import models
from django.utils import timezone
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=255, unique=True)
    gst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    units = models.CharField(max_length=255, default='pcs')
    image = models.ImageField(upload_to='products/', default='products/default.jpg')
    account  = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.unique_id:
            date = timezone.now().strftime("%Y%m%d%H%M%S%f")
            self.unique_id = date + str(self.id)
        super(Product, self).save(*args, **kwargs)
    

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name