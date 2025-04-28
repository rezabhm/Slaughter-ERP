from django.contrib import admin

from apps.product.models import *

# Register your models here.
admin.site.register(Unit)
admin.site.register(ProductCategory)
admin.site.register(Product)
