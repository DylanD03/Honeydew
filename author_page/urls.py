from django.urls import path
from . import views

urlpatterns = [
    #follow request urls cause they are being stinky
    path('accept/<path:author_id>/follow-request/<path:requester_id>/', views.accept_follow_request, name='accept_follow_request'),
    path('deny/<path:author_id>/follow-request/<path:requester_id>/', views.deny_follow_request, name='deny_follow_request'),
    #path('<int:author_id>/follow-request/accept/<int:requester_id>/', views.accept_follow_request, name='accept_follow_request'),
    #path('<int:author_id>/follow-request/deny/<int:requester_id>/', views.deny_follow_request, name='deny_follow_request'),

    #url for author list
    path('authors', views.view_authors, name='view_authors'),

    #urls for serial
    path('<int:author_id>/', views.view_author_profile, name='view_author_profile'),
    path('<int:author_id>/following/', views.view_author_following, name='following'),
    path('<int:author_id>/follower/', views.view_author_followers, name='follower'),
    path('<int:author_id>/follow_request/', views.send_follow_request, name='send_follow_request'),
    path('<int:author_id>/unfollow/', views.unfollow_author, name='unfollow_author'),
    path('<int:author_id>/edit/', views.edit_profile, name='edit_profile'),
    path('<int:author_id>/view-follow-requests/', views.view_follow_requests, name='view_follow_requests'),
    path('<int:author_id>/friends/', views.view_author_friends, name='friend'),

    #Set of URLs for fqid
    path('<path:author_id>/following/', views.view_author_following, name='following'),
    path('<path:author_id>/follower/', views.view_author_followers, name='follower'),
    path('<path:author_id>/follow_request/', views.send_follow_request, name='send_follow_request'),
    path('<path:author_id>/unfollow/', views.unfollow_author, name='unfollow_author'),
    path('<path:author_id>/edit/', views.edit_profile, name='edit_profile'),
    path('<path:author_id>/friends/', views.view_author_friends, name='friend'),
    path('<path:author_id>/', views.view_author_profile, name='view_author_profile'),
]
