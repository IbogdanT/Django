from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import Articles, Comment

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль", required=True, min_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтверждение пароля", required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'type': 'email'}),
        }

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Пароли не совпадают")
        return password_confirm

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Данный пользователь уже существует")
        return username

class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль", required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Неверное имя пользователя или пароль")
            if not user.is_active:
                raise ValidationError("Этот аккаунт неактивен")

class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'anons', 'full_text', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_full_text(self):
        full_text = self.cleaned_data.get('full_text')
        word_count = len(full_text.split())

        if word_count < 50:
            raise ValidationError('Текст статьи должен содержать не менее 50 слов. Сейчас: {}'.format(word_count))

        return full_text

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ваш комментарий...'})
        }
