from django.contrib import admin
from .models import *
from django.db import models

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)