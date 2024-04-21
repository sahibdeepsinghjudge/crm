from django.db import models
from django.utils import timezone
# Create your models here.


class OrderData(models.Model):
    order_id = models.CharField(max_length=255)
    order_status = models.CharField(max_length=255)
    order_cost = models.FloatField(default=0)
    order_total = models.FloatField(default=0)
    order_discount = models.FloatField(null=True, blank=True)
    order_tax = models.FloatField(default=0)
    order_shipping = models.FloatField(null=True, blank=True)
    order_grand_total = models.FloatField(default=0)
    is_online = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    customer = models.CharField(max_length=255)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    products = models.TextField()
    invoice = models.CharField( null=True, blank=True,max_length=10)

    def __str__(self):
        return self.order_id
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            date = timezone.now().strftime("%Y%m%d%H%M%S%f")
            self.invoice = date[:8]
            self.order_id = date
            self.order_grand_total = self.order_total + self.order_tax 
        super(OrderData, self).save(*args, **kwargs)

    def get_products_count(self):
        products = self.products.split(',')
        return len(products)-1
    
    def order_total_price(self):
        return self.order_total + self.order_tax
    
