import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название')
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains', label='Автор')
    created_at = django_filters.DateFilter(lookup_expr='exact', label='Дата публикации')

    class Meta:
        model = Post
        fields = ['title', 'author', 'created_at']