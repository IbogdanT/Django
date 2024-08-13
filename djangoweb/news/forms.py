from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Articles

# Форма регистрации
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтверждение пароля")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

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

# Форма входа
class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Данный аккаунт не существует")
            if not user.is_active:
                raise ValidationError("Этот аккаунт неактивен")

# Форма создания новостей
class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'anons', 'full_text', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
