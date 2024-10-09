from django.urls import path

from . import views


urlpatterns = [
    path('note/<str:id>/', views.view_note, name='view_note'),
]
