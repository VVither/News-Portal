from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post


@receiver(post_save, sender=Post)
def send_new_post_notification(sender, instance, created, **kwargs):
    """Отправляет уведомление о новой статье подписчикам категории"""
    if created:
        for category in instance.categories.all():
            for subscriber in category.subscribers.all():
                # Рендеринг HTML шаблона письма
                html_message = render_to_string('news_email.html', {
                    'title': instance.title,
                    'content': instance.content[:50] + '...',
                    'post_url': instance.get_absolute_url(),  # Получение URL статьи
                    'user': subscriber,  # Передаем объект пользователя в шаблон
                })

                # Отправка письма
                send_mail(
                    subject=f'Новая статья в категории {category.name}',
                    message='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    html_message=html_message,
                )

