from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from django.core.exceptions import ValidationError

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
    
    def get_absolute_url(self):
        if self.post_type == 'NW':
            return reverse("news:news_detail", args=[str(self.id)])
        else: 
            return reverse("news:articles_detail", args=[str(self.id)])    
        
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

        super().save(*args, **kwargs)
        
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
