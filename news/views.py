from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import Http404, HttpResponse
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class PostListView(ListView): # Представление для вывода общего списка
    model = Post
    template_name = 'post_list.html' # Путь к шаблону
    context_object_name = 'posts' # Имя переменной которая будет использоваться в шаблоне 
    ordering = ['-created_at'] # Сортировка от новых к старым
    paginate_by = 10 # Укажите кол-во постов на 1 странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = self.get_queryset().count # Кол-во постов
        context['year'] = timezone.now().year # Текущий год
        return context

class NewsListView(ListView): # Представление для вывода списка новостей
    model = Post
    template_name = 'news/news_list.html' # Путь к шаблону
    context_object_name = 'posts' # Имя переменной которая будет использоваться в шаблоне 
    ordering = ['-created_at'] # Сортировка от новых к старым
    paginate_by = 10 # Укажите кол-во постов на 1 странице

    def get_queryset(self): # Фильтр только новости
        return Post.objects.filter(post_type__in =['Новость', 'NW'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_count'] = self.get_queryset().count # Кол-во постов
        context['year'] = timezone.now().year # Текущий год
        return context
    
class ArticlesListView(ListView): # Представление для вывода списка статей
    model = Post
    template_name = 'articles/articles_list.html' #Путь к шаблону
    context_object_name = 'posts' # Имя переменной которая будет использоваться в шаблоне
    ordering = ['-created_at'] # Сортировка от новых к старым
    paginate_by = 10 # Кол-во постов на странице

    def get_queryset(self):
        return Post.objects.filter(post_type__in = ['Статья', 'AR'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles_count'] = self.get_queryset().count # Кол-во постов
        context['year'] = timezone.now().year # Текущий год
        return context

class NewsDetailView(DetailView): #Представление для вывода детализации новости
    model = Post
    template_name = 'news/news_detail.html' # Путь к шаблону
    context_object_name = 'post' # Имя переменной в шаблоне

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        #post = get_object_or_404(Post, id=self.kwargs['post_id'])
        if post.post_type != 'NW' and post.post_type != 'Новость':
           raise Http404('Это не новость!"')
        return post
    
class ArticlesDetailView(DetailView): # Представление для вывода детализации статей
    model = Post
    template_name = 'articles/articles_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.post_type != 'AR' and post.post_type != 'Статья':
            raise Http404("Это не статья!")
        return post

def search_posts(request): # представление для поиска
    f = PostFilter(request.GET, queryset=Post.objects.all())
    return render(request, 'news/search_result.html', {'filter': f})

class NewsCreate(CreateView): # Представление для создания новостей
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'Новость'
        return super().form_valid(form)

class ArticlesCreate(CreateView): # Представление для создания статей
    form_class = PostForm
    model = Post
    template_name = 'articles/articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'Статья'
        return super().form_valid(form) 

class NewsUpdate(UpdateView): # Представление для создания новостей
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'

class ArticlesUpdate(UpdateView): # Представление для изменения статей
    form_class = PostForm
    model = Post
    template_name = 'articles/articles_edit.html'

class NewsDelete(DeleteView): # Представление для удаления новостей
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news:news_list')

class ArticlesDelete(DeleteView): # Представление для удаления статей
    model = Post
    template_name = 'articles/articles_delete.html'
    success_url = reverse_lazy('news:articles_list')