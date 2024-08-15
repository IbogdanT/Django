from django.shortcuts import render, redirect, get_object_or_404
from .models import Articles, Comment
from .forms import ArticlesForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages  # Импортируем messages

def news_home(request):
    news = Articles.objects.order_by('-date')
    return render(request, 'news/news_home.html', {'news': news})

def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user  # Устанавливаем текущего пользователя
            article.save()
            return redirect('news_home')
        else:
            error = 'Форма была неверной'
    
    form = ArticlesForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'news/create.html', data)

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context['comments'] = article.comments.all()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = article
            comment.user = request.user
            comment.save()
            return redirect('details_view', pk=article.pk)

        return self.get(request, *args, **kwargs)

class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = Articles
    template_name = 'news/create.html'
    form_class = ArticlesForm

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if article.user != request.user:
            return HttpResponseForbidden("У вас нет прав для редактирования этой статьи.")
        return super().dispatch(request, *args, **kwargs)

class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = Articles
    success_url = '/news/'
    template_name = 'news/news-delete.html'

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()
        if article.user != request.user:
            return HttpResponseForbidden("У вас нет прав для удаления этой статьи.")
        return super().dispatch(request, *args, **kwargs)

class UserProfileView(DetailView):
    model = User
    template_name = 'news/user_profile.html'

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['news_count'] = Articles.objects.filter(user=user).count()
        return context

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if not request.user.is_authenticated and user != request.user:
            messages.info(request, "Войдите в аккаунт, чтобы просмотреть профиль автора.")
            return redirect(settings.LOGIN_URL)
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'news/comment_delete.html'
    success_url = '/news/'

    def test_func(self):
        return self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if not self.test_func():
            return HttpResponseForbidden("У вас нет прав для удаления этого комментария.")
        if request.method == 'POST' and self.test_func():
            return self.delete(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
