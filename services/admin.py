from django.contrib import admin
from .models import Category, Services

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'published_date', 'created_date', 'updated_date')
    list_filter = ('status', 'category')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'
    readonly_fields = ('created_date', 'updated_date')
    exclude = ('published_date',) 
    filter_horizontal = ('category',)
    
    

admin.site.register(Services, ServiceAdmin)
