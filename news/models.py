from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    def upgrade_rating(self):
        post_ratings = sum(post.rating * 3 for post in self.post_set.all())
        comment_ratings = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
        author_comment_ratings = sum(comment.rating for post in self.post_set.all() for comment in Comment.objects.filter(post=post))
        self.rating = post_ratings + comment_ratings + author_comment_ratings
        self.save()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscribed_categories')

    def __str__(self):
        return self.name
    
class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    
    POST_TYPE_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.FloatField(default=0)

    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.title  
    
    def get_absolute_url(post):
        if post.post_type == 'NW':
            return reverse("news:news_detail", args=[str(post.id)])
        else:
            return reverse("news:articles_detail", args=[str(post.id)]) 
    
    def _set_categories(self, *args, **kwargs):
            if 'categories' in kwargs:
                categories = kwargs['categories']
                if categories:
                    for category in categories:
                        PostCategory.objects.get_or_create(post=self, category=category)
        
    def send_new_post_notification(self):
        """
        Отправляет уведомление подписчикам категории о создании нового поста.
        """
        for category in self.categories.all():
            for subscriber in category.subscribers.all():
                subject = f"Новый пост в категории {category.name}!"
                message = f"Привет, {subscriber.username}!\n\n"
                message += f"В категории '{category.name}' появился новый пост:\n\n"
                message += f"- {self.title} - {self.get_absolute_url()}\n\n"
                message += "С уважением,\nАдминистрация сайта"
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[subscriber.email],
                    fail_silently=False
                )

    def save(self, *args, **kwargs):
        # Проверка количества публикаций в день
        created_at = date.today()
        if self.author:
            last_posts = Post.objects.filter(
                author=self.author, created_at=created_at
            ).count()
            if last_posts >= 3:
                raise ValidationError(
                    "Вы можете публиковать не более трёх новостей в день."
                )

        self._set_categories(*args, **kwargs)
        super().save(*args, **kwargs)
        self.send_new_post_notification.delay(self.pk) 
            

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['post', 'category']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'

class BadWord(models.Model):
    word = models.CharField(max_length=255)

    def __str__(self):
        return self.word
