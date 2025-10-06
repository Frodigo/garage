from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=self.kwargs['post'],
            published_at__year=self.kwargs['year'],
            published_at__month=self.kwargs['month'],
            published_at__day=self.kwargs['day']
        )
