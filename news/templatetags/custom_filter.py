from django import template
from news.models import BadWord

register = template.Library()

@register.filter(name='censor')
def censor(value):
      """ Заменяет буквы в нежелательных слов в строке на '*' """
      bad_words = BadWord.objects.values_list('word', flat=True)
      
      for word in bad_words:
         value = value.replace(word, '*' * len(word))
      
      return value