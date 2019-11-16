from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario, Topic, Thread, Post

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class NewThreadForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Escribe el contenido'}
        ), 
        max_length=5000,
        help_text='Máximo 5000 caracteres'
        )

    class Meta:
        model = Thread
        fields = ['name', 'body']

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body', ]

