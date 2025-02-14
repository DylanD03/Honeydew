from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from requests.auth import HTTPBasicAuth
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from django.urls import include, path
from django.conf import settings
from api.authentication import encode_basic_auth
import socket
import os



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


class HandleNodeConnectionTest(APITestCase):
    """
    Testing Remote Node Connectivity
    Running test Suite:
        python manage.py test api.tests.HandleNodeConnectionTest

    From Project Description:
        You could write a test that adds a node to connect with by calling
        Python code or modifying the database directly, then use the API
        to check that the new node connection is working.
    """
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        # Default Username/Password to Access our API.
        self.AUTH_USERNAME = settings.AUTH_USERNAME
        self.AUTH_PASSWORD = settings.AUTH_PASSWORD

        self.valid_headers = {
            'Authorization': encode_basic_auth(self.AUTH_USERNAME, self.AUTH_PASSWORD)
        }

        self.invalid_headers = {
            'Authorization': encode_basic_auth(self.AUTH_USERNAME+'invalid', self.AUTH_PASSWORD+'invalid')
        }

        # Get the API endpoint to our node authenticator
        self.auth_url = f"{SERVER}/api/auth/"
        self.test_auth_url = f"{SERVER}/api/auth/test"
        
        # Enable connections to this node
        Node.objects.create(
            host="testserver",
            our_username=self.AUTH_USERNAME,
            our_password=self.AUTH_PASSWORD,
            enable_connection=True
        )
        

    def test_valid_authentication(self):
        """
        Test valid authentication with correct username and password in the query parameters.
        """
        # Authentificate using valid Username/Password
        response = self.client.get(self.auth_url, **self.valid_headers)

        # Assert Successfull authentification
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_authentication(self):
        """
        Test invalid authentication with incorrect username and password.
        """
        # Authentificate using invalid Username/Password
        response = self.client.get(self.auth_url, **self.invalid_headers)

        # Check if the response status is 401 (unauthorized authentification)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_request_with_authentication(self):
        """
        Test if POST requests works with authentification
        python manage.py test api_tests.tests.HandleNodeConnectionTest.test_post_request_with_authentication
        """
        # Authentificate using valid Username/Password
        # Send a POST request using valid Username/Password
        post_data = {'some_key': 'some_value'}
        response = self.client.post(self.test_auth_url, data=post_data, **self.valid_headers)

        # POST request should be successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_post_request_without_authentication(self):
        """
        Test if POST requests works WITHOUT authentification
        python manage.py test api_tests.tests.HandleNodeConnectionTest.test_post_request_without_authentication
        """
        # Authentificate using invalid Username/Password
        # Send a POST request using invalid Username/Password
        post_data = {'some_key': 'some_value'}  # Data for the POST request
        response = self.client.post(self.test_auth_url, data=post_data, **self.invalid_headers)

        # POST request should be UNsuccessful
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    def tearDown(self):
        Node.objects.all().delete()  
        LocalUser.objects.all().delete()
        Post.objects.all().delete()
        Author.objects.all().delete()
        Like.objects.all().delete
        Comment.objects.all().delete
        Follow.objects.all().delete
