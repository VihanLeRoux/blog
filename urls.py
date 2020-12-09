from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.BlogView.as_view(), name='blog'),
    path('post/<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path('post/new/', views.PostFormView().as_view(), name='new_post'),
    path('drafts/', views.DraftView.as_view(), name='draft_list'),
    path('post/<int:pk>/publish/', views.publish, name='publish'),
    path('post/<int:pk>/remove/', views.remove, name='remove'),
    path('post/<int:pk>/edit/', views.edit, name='edit'),
]