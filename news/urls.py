from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PostListView, PostSearchView, UserRegisterView, UserLoginView
from .views import NewsListView, NewsDetailView, NewsCreate, NewsUpdate, NewsDelete
from .views import ArticlesCreate, ArticlesDetailView, ArticlesListView, ArticlesUpdate, ArticlesDelete

app_name = 'news'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name= 'logout'),
    path('post/', PostListView.as_view(), name='post_list'), # Общий список
    path('post/news/', NewsListView.as_view(), name='news_list'), # Cписок новостей
    path('post/news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'), # Детализация новости
    path('post/news/search/', PostSearchView.as_view(), name='search'), # Поиск
    path('post/news/create/', NewsCreate.as_view(), name='news_create'), # Создание новостей
    path('post/news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'), # Редактирование новостей
    path('post/news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'), # Подтверждение удаления новости
    path('post/articles/', ArticlesListView.as_view(), name='articles_list'), # Список статей
    path('post/articles/<int:pk>/', ArticlesDetailView.as_view(), name='articles_detail'), # Детализация статьи
    path('post/articles/create', ArticlesCreate.as_view(), name='articles_create'), # Создание статьи
    path('post/articles/<int:pk>/update/', ArticlesUpdate.as_view(), name='articles_update'), # Редактирование статьи
    path('post/articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'), # Подтверждение удаления статьи

]
