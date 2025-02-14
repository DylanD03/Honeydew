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

class HandleCommentTest(APITestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        for i in range(2):
            author = gen_author()
            for i in range(2):
                post = gen_post(author)
                # Author comments on each of their own post 3 times
                for i in range(3):
                    gen_comment(author, post)

        self.user = gen_user()

    def test_handle_author_commented(self):
        response = client.get(f"{SERVER}/api/authors/1/commented")
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()
        assert len(data) == 5, f"Recieved: {len(data)}"
        
        # Author does not have any comments.
        response = client.get(f"{SERVER}/api/authors/3/commented")
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()
        assert len(data) == 0, f"Recieved: {len(data)}"

        # TODO Also throw in some POSTs
        

    def test_get_author_commented_fqid(self):
        author = Author.objects.get(serial=1)

        response = client.get(f"{SERVER}/api/authors/{author.fqid}/commented")
        assert response.status_code == 200, f"Recieved: {response.status_code}"

        # Commenting on other author's post.
        author2 = gen_author()
        author3 = gen_author()
        post = gen_post(author2)
        response = client.get(f"{SERVER}/api/posts/{post.fqid}/comments")

        # no comments on this post.
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()
        assert data["count"] == 0, f"Recieved: {data['count']}"

        gen_comment(author3, post) # author3 commented on author2s post.
        response = client.get(f"{SERVER}/api/posts/{post.fqid}/comments")
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()
        assert data["count"] == 1, f"Recieved: {data['count']}"

        


    def tearDown(self):
        Author.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()
