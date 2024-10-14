from django.urls import path

from . import views


urlpatterns = [
    path('note/<str:id>/', views.view_note, name='view_note'),
    path('', views.user_notes, name='user_notes'),
    path('create/',views.create_note , name='create_note')
]
