from django.db import models
from django.conf import settings

class Articles(models.Model):
    title = models.CharField('Название', max_length=50)
    anons = models.CharField('Анонс', max_length=250)
    full_text = models.TextField('Статья')
    date = models.DateTimeField('Дата публикации')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    published = models.BooleanField(default=False, verbose_name='Опубликована')

    def __str__(self):
        return f'Новость: {self.title}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('news-details', args=[self.id])

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['user']),
        ]

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f'Профиль пользователя: {self.user.username}'

class Comment(models.Model):
    news = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.news.title}"
