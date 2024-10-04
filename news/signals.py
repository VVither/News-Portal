from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Post

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        subscribers = instance.categories.values_list('subscribers__email', flat=True)
        for email in subscribers:
            subject = f'Новая статья в категории {", ".join(instance.categories.values_list("name", flat=True))}'
            html_content = render_to_string('news_email.html', {
                'title': instance.title,
                'content': instance.content[:50],  # первые 50 символов контента
            })
            send_mail(subject, '', 'from@example.com', [email], html_message=html_content)