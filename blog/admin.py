from django.contrib import admin
from .models import Post, Category, Comment
from django.utils.translation import gettext_lazy as _
from django_jalali.admin.filters import JDateFieldListFilter


class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('title', 'author', 'counted_views', 'status',
                    'published_date', 'created_date')
    # list_filter = ('status', 'author')
    list_filter = ('status', 'author', ('created_date', JDateFieldListFilter))
    search_fields = ['title', 'content']
    filter_horizontal = ('category',)
    readonly_fields = ('counted_comment',)
    exclude = ('counted_views',) 

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'post', 'approved', 'created_date', 'updated_date')
    list_filter = ('approved', 'created_date', 'updated_date')
    search_fields = ('name', 'phone_number', 'message')
    list_editable = ('approved',)
    date_hierarchy = 'created_date'
    readonly_fields = ('created_date', 'updated_date')

    fieldsets = (
        ('Comment Details', {
            'fields': ('name', 'email', 'phone_number', 'message', 'post'),  # Include 'post' in the fields
            'classes': ('wide',),
        }),
        ('Approval', {
            'fields': ('approved',),
        }),
        ('Dates', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse', 'wide'),
        }),
    )

    # Customize the display name for the 'post' field
    def post(self, obj):
        return obj.post.title
    post.short_description = 'Post Title'

    # Override the 'save_model' method to automatically set the author
    def save_model(self, request, obj, form, change):
        if not obj.post:
            # Set a default post (e.g., General post) when no post is specified
            obj.post = Post.objects.get_or_create(title="General")[0]
        super().save_model(request, obj, form, change)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
