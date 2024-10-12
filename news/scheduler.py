from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from news.models import Post, Category
from django.utils import timezone

def send_weekly_emails():
    categories = Category.objects.all()
    for category in categories:
        # Получаем подписчиков этой категории
        subscribers = category.subscribers.all()
        # Получаем новые посты за последнюю неделю
        new_posts = Post.objects.filter(category=category, created_at__gte=timezone.now()-timezone.timedelta(weeks=1))
        
        # Отправка email каждому подписчику
        for subscriber in subscribers:
            if new_posts.exists():
                post_titles = ', '.join([post.title for post in new_posts])
                send_mail(
                    f'Новые посты в категории {category.name}',
                    f'Посты: {post_titles}',
                    'from@example.com',  # укажите здесь ваш email
                    [subscriber.email],
                    fail_silently=False,
                )

# Настройка APScheduler
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_weekly_emails, 'interval', weeks=1)
    scheduler.start()