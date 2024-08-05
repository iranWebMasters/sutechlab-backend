from django.urls import path
from .views import HomeView, BlogListView, BlogDetailView, BlogSearchView
app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='index'),
    path('blog/<str:cat_name>/', BlogListView.as_view(), name='blog_list_category'),
    path('blog/<str:username>/', BlogListView.as_view(), name='blog_list_author'),
    path('blog/tag/<str:tag_name>/', BlogListView.as_view(), name='tag'),

    # Define URL pattern for the blog detail page with post ID parameter
    path('<int:pk>/', BlogDetailView.as_view(), name='single'),

    # Define URL pattern for the blog search page
    path('search/', BlogSearchView.as_view(), name='search'),
]
