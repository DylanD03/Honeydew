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
from api.authentication import encode_basic_auth
from django.db.models import Q
# Load environment variables from .env file
load_dotenv()
SERVER = "http://testserver"
client = APIClient()

class HandlePostTest(APITestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
           urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        # Default Username/Password to Access our API.
        
        #public 
        self.author1 = gen_author()
        for i in range(6):
            gen_post(self.author1)

        #friends
        self.author2 = gen_author()
        self.a2p1fqid = None
        self.a2p1deleted = None

        for i in range(7):
            if i ==6:
                v = gen_post(self.author2, visibility= Post.DELETED)
                self.a2p1deleted = v.fqid

            p = gen_post(self.author2, visibility= Post.FRIENDS)
            if i == 2:
                self.a2p1fqid = p.fqid


        self.author3 = gen_author()
        gen_post(self.author3, visibility= Post.FRIENDS)

        self.user = gen_user()
        self.userowner = gen_user(author = self.author2)  #owner

    def test_handle_post_anonymous(self):
        response = client.get(f"{SERVER}/api/authors/1/posts/1")
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()
        data["title"] = "New Title!"

        # Disallowed Methods
        response = client.post(f"{SERVER}/api/authors/2/posts/1")
        assert response.status_code == 405, f"Recieved: {response.status_code}"


    def test_handle_post_loggedin(self):
        #log in, specify the ending user, and make it a friend of author1
        client.force_authenticate(user=self.user)

        #author2 uses friendship only

        #No friendship
        response = client.get(f"{SERVER}/api/authors/2/posts/5")
        assert response.status_code == 401, f"Recieved: {response.status_code}"

        gen_follow(self.author2, self.user.author)
        gen_follow(self.user.author, self.author2)

        #for author2 with friends post
        response = client.get(f"{SERVER}/api/authors/2/posts/5")
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        #I get 404 error...

        #even as an authenticationed friend, I cannot delete/put the data
        response = client.put(f"{SERVER}/api/authors/2/posts/2")
        assert response.status_code == 401, f"Recieved: {response.status_code}"
        response = client.delete(f"{SERVER}/api/authors/2/posts/2")
        assert response.status_code == 401, f"Recieved: {response.status_code}"


        #PUT and DELETE methods can only be done by the owner of the post
        client.force_authenticate(user=None)
        client.force_authenticate(user=self.userowner)

        post_data = {'some_key': 'some_value'}
        response = client.put(f"{SERVER}/api/authors/2/posts/2", data = post_data)
        assert response.status_code == 200, f"Recieved: {response.status_code}"

        response = client.delete(f"{SERVER}/api/authors/2/posts/2")
        assert response.status_code == 200, f"Recieved: {response.status_code}"

        #unregistered method
        response = client.post(f"{SERVER}/api/authors/2/posts/2")
        assert response.status_code == 405, f"Recieved: {response.status_code}"

        client.force_authenticate(user=None)

    def test_get_fqid_post(self):
        client.force_authenticate(user=self.user)
        fqid = self.a2p1fqid
        fqdelete = self.a2p1deleted
        response = client.get(f"{SERVER}/api/posts/{fqid}")
        assert response.status_code == 401, f"Recieved: {response.status_code}"

        #preauthentication
        client.force_authenticate(user=None)
        client.force_authenticate(user=self.userowner)

        response = client.get(f"{SERVER}/api/posts/{fqid}")
        assert response.status_code == 200, f"Recieved: {response.status_code}"

        response = client.delete(f"{SERVER}/api/posts/{fqdelete}")
        assert response.status_code == 405, f"Recieved: {response.status_code}"

        

    def tearDown(self):
        Author.objects.all().delete()
        Post.objects.all().delete()
        LocalUser.objects.all().delete()