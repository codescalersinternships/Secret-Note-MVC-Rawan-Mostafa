from django.urls import path
from django_ratelimit.decorators import ratelimit
from . import views


urlpatterns = [
    path('note/<str:id>/', views.view_note, name='view_note'),
    path('', views.user_notes, name='user_notes'),
    path('create/', ratelimit(key='user_or_ip', rate='10/m', method='POST', block=True)(views.create_note) , name='create_note')
]
