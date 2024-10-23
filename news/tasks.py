from datetime import date, timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Category, Post


@shared_task
def send_weekly_email():
    """
    Отправляет еженедельную рассылку email подписчикам категорий о новых постах.
    """
    last_week_start = (date.today() - timedelta(days=date.today().weekday() + 7)).isoformat()
    last_week_end = (date.today() - timedelta(days=date.today().weekday() + 1)).isoformat()

    for category in Category.objects.all():
        new_posts = Post.objects.filter(
            categories=category, 
            created_at__gte=last_week_start, 
            created_at__lte=last_week_end
        )
        if new_posts:
            for subscriber in category.subscribers.all():
                subject = f"Новые посты в категории {category.name} за прошедшую неделю"
                message = f"Привет, {subscriber.username}!\n\n"
                message += f"В категории '{category.name}' появились новые посты за прошлую неделю:\n\n"
                for post in new_posts:
                    message += f"- {post.title} - {post.get_absolute_url()}\n"
                message += "\nС уважением,\nАдминистрация сайта"
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[subscriber.email],
                    fail_silently=False
                )
