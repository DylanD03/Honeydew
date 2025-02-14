from django.urls import path
from . import views

from django.shortcuts import render

urlpatterns = [
    path('', views.stream_home, name='stream-home'),
    path("post/<path:id>/", views.view_post, name="view_post"),
]