from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from requests.auth import HTTPBasicAuth
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from django.urls import include, path
from django.conf import settings

from .model_gen import gen_author, gen_user, gen_post,\
    gen_follow, gen_like, gen_comment
from api.serializers import AuthorSerializer, AuthorsSerializer,\
    FollowRequestSerializer, FollowersSerializer, PostSerializer, \
    CommentSerializer, CommentsSerializer, LikeSerializer
from honeydew.models import LocalUser, Author, Post, Like, Comment, Follow, \
    FollowRequest, Friendship, Node

# Load environment variables from .env file
load_dotenv()
SERVER = "http://testserver"
client = APIClient()


class GetImageTest(APITestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        print("*** GetImageTest ***")
        self.author = gen_author()
        self.friend = gen_author()
        self.public = gen_post(self.author, content_type=Post.IMAGE, visibility=Post.PUBLIC)
        self.unlisted = gen_post(self.author, content_type=Post.IMAGE, visibility=Post.PUBLIC)
        self.friends = gen_post(self.author, content_type=Post.IMAGE, visibility=Post.PUBLIC)

        gen_follow(self.author, self.friend)
        gen_follow(self.friend, self.author)

    def test_get_serial(self):
        response = client.get(f"{SERVER}/api/authors/{self.author.serial}/posts/{self.public.serial}/image")
        assert response.status_code == 200, f"Recieved {response.status_code}"

    def test_get_fqid(self):
        response = client.get(f"{SERVER}/api/posts/{self.public.fqid}")
        assert response.status_code == 200, f"Recieved {response.status_code}"
