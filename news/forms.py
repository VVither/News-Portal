from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError

from .models import Post


class UserRegistrationForm(UserCreationForm): # Форма регистрации
    email = forms.EmailField()    
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class PostForm(forms.ModelForm): # Форма для поиска
    class Meta:
        model = Post
        fields = [
            'author',
            'categories',
            'title',
            'content',
        ]

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        if content is not None and len(content) < 20:
            raise ValidationError({
                'content': "Описание не может содержат менее 20 символов"
            })
        
        name = cleaned_data.get('title')
        if name == content:
            raise ValidationError(
                "Описание не может быть идентично названию"
            )
        if name[0].islower():
            raise ValidationError(
                "Название должно быть с заглавной буквы"
            )
        return cleaned_data

class BasicSingupForm(SignupForm):

    def save(self, request):
        user = super(BasicSingupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
