from django.db import models
from django.contrib.auth.models import User  

# Create your models here.
# --------------------------------------------------------------------


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# --------------------------------------------------------------------


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)  
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()  
    image = models.ImageField(upload_to='car_images/')  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.brand.name}'


# -------------------------------------------------------------------------


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    car = models.ForeignKey(Car, on_delete=models.CASCADE)   
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'



# --------------------------------------------------------------------------

class Comment(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  
    name = models.CharField(max_length=255)                 
    comment = models.TextField()                            
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f'Comment by {self.name} on {self.car.title}'
