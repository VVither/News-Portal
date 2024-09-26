from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'post_type',
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






