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


class GetAuthorsTest(APITestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        for i in range(13):
            gen_author()

    def test_get_authors(self):
        response = client.get(f"{SERVER}/api/authors/")
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()
        assert data['type'] == "authors"
        assert len(data['authors']) == 5

    def test_page_cutoff(self):
        response = client.get(f"{SERVER}/api/authors/?page=4")
        assert response.status_code == 404, f"Recieved: {response.status_code}"

        response = client.get(f"{SERVER}/api/authors/?page=3")
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()
        assert data['type'] == "authors", f"Recieved: {data['type']}"
        assert len(data['authors']) == 3, f"Recieved: {len(data['authors'])}"

    def test_page_size(self):
        response = client.get(f"{SERVER}/api/authors/?size=3")
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()
        assert data['type'] == "authors", f"Recieved: {data['type']}"
        assert len(data['authors']) == 3, f"Recieved: {len(data['authors'])}"

        response = client.get(f"{SERVER}/api/authors/?page=5&size=3")
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()
        assert data['type'] == "authors", f"Recieved: {data['type']}"
        assert len(data['authors']) == 1, f"Recieved: {len(data['authors'])}"

    def test_negative_query(self):
        response = client.get(f"{SERVER}/api/authors/?size=-5")
        assert response.status_code == 404, f"Recieved: {response.status_code}"
        response = client.get(f"{SERVER}/api/authors/?page=-1")
        assert response.status_code == 404, f"Recieved: {response.status_code}"
        response = client.get(f"{SERVER}/api/authors/?page=-3&size=-5")
        assert response.status_code == 404, f"Recieved: {response.status_code}"

    # TODO Test for authentication
    def test_author_serial(self):
        response = client.get(f"{SERVER}/api/authors/5")
        assert response.status_code == 200, f"Recieved: {response.status_code}"

        data = response.json()
        assert data["type"] == "author"

        #check last test case.
        auth = Author.objects.get(serial=1)
        serauth = AuthorSerializer(auth)
        response3 = client.post(f"{SERVER}/api/authors/5", data = serauth.data)

        assert response3.status_code == 405, f"Recieved: {response.status_code}"
    # TODO Test for authentication

    def test_author_fqid(self):
        ####How do I make an example Author with an FQID to add it?
        auth = Author.objects.get(serial = 1)
        fqid = auth.fqid
        response = client.get(f"{SERVER}/api/authors/" + fqid)
        assert response.status_code == 200, f"Recieved: {response.status_code}"

    def tearDown(self):
        Author.objects.all().delete()
