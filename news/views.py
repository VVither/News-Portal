from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth import views as auth_views
from django.db.models.base import Model as Model
#from django.db.models.query import QuerySet
#from django.forms.models import BaseModelForm
#from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils import timezone
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import Http404
from .models import Post, Category
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

    def get_context_data(self, **kwargs ):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['categories'] = post.categories.all()
        return context
    
class ArticlesDetailView(DetailView): # Представление для вывода детализации статей
    model = Post
    template_name = 'articles/articles_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.post_type != 'AR' and post.post_type != 'Статья':
            raise Http404("Это не статья!")
        return post

class PostSearchView(ListView): # Представление для поиска
    model = Post
    template_name = 'news/search_result.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = self.filterset
        return context

class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin,CreateView): # Представление для создания новостей
    permission_required = ('post.add_object', )
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'Новость'
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

class ArticlesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView): # Представление для создания статей
    permission_required = ('post.add_object', )
    form_class = PostForm
    model = Post
    template_name = 'articles/articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'Статья'
        return super().form_valid(form) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

class NewsUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # Представление для создания новостей
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'

    def test_func(self):
        post = self.get_object()  # Получаем объект поста
        return self.request.user == post.author or self.request.user.is_staff

class ArticlesUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # Представление для изменения статей
    form_class = PostForm
    model = Post
    template_name = 'articles/articles_edit.html'

    def test_func(self):
        post = self.get_object()  # Получаем объект поста
        return self.request.user == post.author or self.request.user.is_staff

class NewsDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # Представление для удаления новостей
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news:news_list')

    def test_func(self):
        post = self.get_object()  # Получаем объект поста
        return self.request.user == post.author or self.request.user.is_staff

class ArticlesDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # Представление для удаления статей
    model = Post
    template_name = 'articles/articles_delete.html'
    success_url = reverse_lazy('news:articles_list')

    def test_func(self):
        post = self.get_object()  # Получаем объект поста
        return self.request.user == post.author or self.request.user.is_staff

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.post_set.all()
        return context
    
@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/post/')

@login_required
def profile_view(request):
    user = request.user
    is_author = user.groups.filter(name='author').exists()

    return render(request, 'post_list.html', {'is_author': is_author})

@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.user.is_authenticated:
        if request.user in category.subscribers.all():
            category.subscribers.remove(request.user)
            message = "Вы отписались от этой категории."
        else:
            category.subscribers.add(request.user)
            message = "Вы подписались на эту категорию!"
        return redirect('news:category_list')
    else:
        return redirect('login')  # Перенаправьте на страницу входа, если пользователь не авторизован

