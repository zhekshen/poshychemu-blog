from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, UserSurvey

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Электронная почта")

    class Meta:
        model = User
        fields = ['username', 'email']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ваш комментарий...'}),
        }

class UserSurveyForm(forms.ModelForm):
    class Meta:
        model = UserSurvey
        fields = ['fishing_experience', 'favorite_fish', 'preferred_gear', 'about_me']
        widgets = {
            'fishing_experience': forms.Select(attrs={'class': 'form-select'}),
            'favorite_fish': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_gear': forms.TextInput(attrs={'class': 'form-control'}),
            'about_me': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
