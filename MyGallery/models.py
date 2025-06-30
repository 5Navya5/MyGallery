from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_with=models.ManyToManyField(User,related_name='shared_product',blank=True)
    name=models.CharField(max_length=255)
    description=models.TextField()
    image=models.ImageField(upload_to='products/',blank=True, null=True)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def edit(self,name,description,image):
        self.name=name
        self.description=description
        self.image=image
        self.save()

class Comments(models.Model):
    product=models.ForeignKey(Product,related_name="comments",on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    body=models.TextField()
    created_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"comment on {self.name} on {self.product.name}"
    def edit(self,name,body):
        self.name=name
        self.body=body
        self.save()

