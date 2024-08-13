from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from news.forms import RegisterForm, LoginForm

def index(request):
    return render(request, 'main/index.html', {'title': 'Главная страница'})

def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш аккаунт был создан. Вы можете войти.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'register_form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'login_form': form})

@login_required
def create_news(request):
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость успешно создана.')
            return redirect('news_home')
    else:
        form = ArticlesForm()
    return render(request, 'main/create_news.html', {'form': form})
