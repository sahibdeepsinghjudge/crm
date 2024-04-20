from django.db import models
from django.utils import timezone
# Create your models here.


class OrderData(models.Model):
    order_id = models.CharField(max_length=255)
    order_status = models.CharField(max_length=255)
    order_total = models.FloatField(default=0)
    order_discount = models.FloatField(null=True, blank=True)
    order_tax = models.FloatField(default=0)
    order_shipping = models.FloatField(null=True, blank=True)
    order_grand_total = models.FloatField(default=0)
    is_online = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE,null=True, blank=True)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    products = models.TextField()

    def __str__(self):
        return self.order_id
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            date = timezone.now().strftime("%Y%m%d%H%M%S%f")
            self.order_id = date
        super(OrderData, self).save(*args, **kwargs)
