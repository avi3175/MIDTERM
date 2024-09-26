from django.contrib import admin
from .models import Brand, Car, Order, Comment

# Register your models here.



admin.site.register(Brand)
admin.site.register(Car)
admin.site.register(Order)
admin.site.register(Comment)
