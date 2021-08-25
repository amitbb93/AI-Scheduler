from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('schedule/', views.schedule, name='schedule-page'),
    path('submitting/', views.submitting, name='submitting-page'),
    path('offer_swap/', views.offer_swap, name='offer_swap-page'),
    path('requests/', views.requests, name='requests-page'),
    path('create/', views.create, name='create-page'),
    path('edit/', views.edit, name='edit-page'),
    path('my_requests/', views.my_requests, name='my_requests-page'),
]
