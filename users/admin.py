from django.contrib import admin
from .models import Admin, Clerk, Collector, Farmer, Route

# Register your models here.
admin.site.register(Admin)
admin.site.register(Clerk)
admin.site.register(Collector)
admin.site.register(Farmer)
admin.site.register(Route)

