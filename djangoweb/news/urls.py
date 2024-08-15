from django.urls import path
from . import views
from main import views as main_views  # Import views from the main app

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='details_view'),
    path('<int:pk>/update/', views.NewsUpdateView.as_view(), name='news-update'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news-delete'),
    path('user/<str:username>/', views.UserProfileView.as_view(), name='user-profile'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

    # Add these lines to include URLs from the main app
    path('login/', main_views.login_view, name='login'),
    path('register/', main_views.register_view, name='register'),
]
