from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Board, Image

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))

class BoardForm(forms.ModelForm):
    images = forms.ModelMultipleChoiceField(
        queryset=Image.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Board
        fields = ['title', 'description', 'images']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["url", "alt_text", "category"]