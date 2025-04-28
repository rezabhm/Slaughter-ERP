from django.contrib import admin

from apps.core.models.ownership import *
from apps.core.models.transportation import *

# Register your models here.
admin.site.register(City)
admin.site.register(Agriculture)
admin.site.register(ProductOwner)
admin.site.register(Car)
admin.site.register(Driver)
