from django.contrib import admin

from .models import Blog , Topic , Comments

admin.site.register(Topic)
admin.site.register(Blog)
admin.site.register(Comments)