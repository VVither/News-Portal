from django.urls import path
from .views import PostListView, search_posts
from .views import NewsListView, NewsDetailView, NewsCreate, NewsUpdate, NewsDelete
from .views import ArticlesCreate, ArticlesDetailView, ArticlesListView, ArticlesUpdate, ArticlesDelete

app_name = 'news'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'), # Общий список
    path('news/', NewsListView.as_view(), name='news_list'), # Cписок новостей
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'), # Детализация новости
    path('news/search/', search_posts, name='search'), # Поиск
    path('news/create/', NewsCreate.as_view(), name='news_create'), # Создание новостей
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'), # Редактирование новостей
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'), # Подтверждение удаления новости
    path('articles/', ArticlesListView.as_view(), name='articles_list'), # Список статей
    path('articles/<int:pk>/', ArticlesDetailView.as_view(), name='articles_detail'), # Детализация статьи
    path('articles/create', ArticlesCreate.as_view(), name='articles_create'), # Создание статьи
    path('articles/<int:pk>/update/', ArticlesUpdate.as_view(), name='articles_update'), # Редактирование статьи
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'), # Подтверждение удаления статьи

]
