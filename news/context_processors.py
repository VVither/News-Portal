from django.contrib.auth.models import Group


def user_context(request):
    is_author = request.user.groups.filter(name='author').exists() if request.user.is_authenticated else False
    return {
        'is_author': is_author,
    }