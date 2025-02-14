from django.urls import path
from .views import *

app_name = 'post'
urlpatterns = [
    path('create/', create_post, name='create_post'), 
    path('type/', get_type, name='get_post_type'),
    path('', index, name='index'),
    path("<path:fqid>/delete/", delete_post, name="delete_post"),
    path("<path:fqid>/edit/", edit_post, name="edit_post"),
    path("<path:fqid>/edit/save/", save_edit, name="save_edit"),
    path("<path:fqid>/comment/create", create_comment, name="create_comment"),
    
]