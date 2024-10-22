from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (ArticlesCreate, ArticlesDelete, ArticlesDetailView,
                    ArticlesListView, ArticlesUpdate, CategoryDetailView,
                    CategoryListView, NewsCreate, NewsDelete, NewsDetailView,
                    NewsListView, NewsUpdate, PostListView, PostSearchView,
                    profile_view, subscribe_to_category, upgrade_me)

app_name = 'news'

urlpatterns = [
    # path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', profile_view, name='profile_view'),
    path('upgrade/', upgrade_me, name= 'upgrade'),
    path('post/', cache_page(60*5)(PostListView.as_view()), name='post_list'), # Общий список
    path('post/news/', cache_page(60*5)(NewsListView.as_view()), name='news_list'), # Cписок новостей
    path('post/news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'), # Детализация новости
    path('post/news/search/', PostSearchView.as_view(), name='search'), # Поиск
    path('post/news/create/', NewsCreate.as_view(), name='news_create'), # Создание новостей
    path('post/news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'), # Редактирование новостей
    path('post/news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'), # Подтверждение удаления новости
    path('post/articles/', cache_page(60*5)(ArticlesListView.as_view()), name='articles_list'), # Список статей
    path('post/articles/<int:pk>/', ArticlesDetailView.as_view(), name='articles_detail'), # Детализация статьи
    path('post/articles/create', ArticlesCreate.as_view(), name='articles_create'), # Создание статьи
    path('post/articles/<int:pk>/update/', ArticlesUpdate.as_view(), name='articles_update'), # Редактирование статьи
    path('post/articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'), # Подтверждение удаления статьи
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:category_id>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category/<int:category_id>/subscribe/', subscribe_to_category, name='subscribe_to_category'),    
]
