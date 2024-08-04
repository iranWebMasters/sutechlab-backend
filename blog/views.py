from django.shortcuts import render
from django.conf.urls import handler404
from django.views.generic import ListView
from django.views import View
from django.shortcuts import render
from .models import Post,Comment
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse 
from django.http import QueryDict
from django.views.generic import DetailView



class HomeView(View):
    template_name = 'blog/blog-home.html'

    def get(self, request):
        return render(request, self.template_name)
    
class BlogListView(ListView):
    model = Post
    template_name = 'blog/blog-home.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        current_time = timezone.now()
        queryset = Post.objects.filter(status=True, published_date__lte=current_time).order_by('-published_date')

        cat_name = self.kwargs.get('cat_name')
        if cat_name:
            queryset = queryset.filter(category__name=cat_name)

        username = self.kwargs.get('username')
        if username:
            queryset = queryset.filter(author__username=username)

        tag_name = self.kwargs.get('tag_name')
        if tag_name:
            queryset = queryset.filter(tags__name=tag_name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch tags for each post and include them in the context
        for post in context['posts']:
            post.tags = post.tags.all()
        return context
    
class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/blog-single.html'
    context_object_name = 'post'
    form_class = CommentForm 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_time = timezone.now()
        all_posts = Post.objects.filter(status=True, published_date__lte=current_time).order_by('-published_date')
        current_index = list(all_posts).index(self.object)
        context['previous_post'] = all_posts[current_index - 1] if current_index > 0 else None
        context['next_post'] = all_posts[current_index + 1] if current_index < len(all_posts) - 1 else None
        context['comments'] = Comment.objects.filter(post=self.object, approved=True).order_by('-created_date')
        context['comment_form'] = CommentForm(initial=self.get_initial_data())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)  # فرم را با استفاده از form_class نمونه‌سازی کنید
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        messages.success(self.request, 'ثبت با موفقیت انجام شد')
        return redirect(self.request.path_info)

    def form_invalid(self, form):
        messages.error(self.request, ' در ثبت فرم خطایی رخ داده است')
        return self.render_to_response(self.get_context_data(form=form))

    def get_initial_data(self):
        initial_data = {}
        if self.request.user.is_authenticated:
            initial_data['name'] = self.request.user.username
            initial_data['email'] = self.request.user.email
        return initial_data
    
class BlogSearchView(ListView):
    model = Post
    template_name = 'blog/blog-home.html'
    context_object_name = 'posts'
    paginate_by = 10
    def get_queryset(self):

        query = self.request.GET.get('s')  # Retrieve the 's' parameter from the GET request
        queryset = super().get_queryset().filter(status=1)  # Filter posts by status
        if query:
            # Use 'icontains' for case-insensitive search in both title and content
            queryset = queryset.filter(title__icontains=query) | queryset.filter(content__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('s', '')  # Pass the search query to the template
        return context
