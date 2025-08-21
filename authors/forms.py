from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        #exclude = ['first_name']

        labels ={
            'username':'Username',
            'first_name':'First Name',
            'last_name':'Last Name',
            'email': 'E-mail',
            'password':'Password'

        }

        help_texts = {
            'email': 'The e-mail must be valid'
        }