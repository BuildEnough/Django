from django import forms
from . import Sign_up

class Sign_upForm(forms.ModelForm):
    class Meta:
        model = Sign_up
        fields = "__all__"