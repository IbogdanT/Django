from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from news.forms import RegisterForm, LoginForm
from news.models import Articles

def index(request):
    return render(request, 'main/index.html', {'title': 'Главная страница'})

def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Данный аккаунт не существует')
    return render(request, 'main/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            password_confirm = form.cleaned_data.get('password_confirm')

            if password != password_confirm:
                form.add_error('password_confirm', 'Пароли не совпадают')
            else:
                if User.objects.filter(username=username).exists():
                    form.add_error('username', 'Данный пользователь уже существует')
                else:
                    User.objects.create_user(username=username, password=password, email=email)
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        auth_login(request, user)
                        return redirect('profile')  # Перенаправление на страницу профиля после регистрации
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})



def logout_view(request):
    auth_logout(request)
    return redirect('login')

def profile_view(request):
    user = request.user
    articles_count = Articles.objects.filter(user=user).count()
    return render(request, 'main/profile.html', {
        'user': user,
        'articles_count': articles_count,
        'registration_date': user.date_joined,
    })

