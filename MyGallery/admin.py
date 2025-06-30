from django.contrib import admin
from .models import Product,Comments

class ProductAdmin(admin.ModelAdmin):
    list_display=('name','description','image')
    search_fields=('name','description')

admin.site.register(Product,ProductAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display=('name','body','product','created_at')
    search_fields=('created_at','name')

admin.site.register(Comments,CommentAdmin)
