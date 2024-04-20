from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Account(models.Model):
    phone = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unique_id = models.CharField(max_length=255, unique=True)
    gst = models.CharField(max_length=15, default='N/A')
    fssai = models.CharField(max_length=14, default='N/A')
    image = models.ImageField(upload_to='accounts/', default='accounts/default.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.phone
        super(Account, self).save(*args, **kwargs)