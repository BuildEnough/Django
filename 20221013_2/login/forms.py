from django import forms
from .models import Article


class LoginForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
