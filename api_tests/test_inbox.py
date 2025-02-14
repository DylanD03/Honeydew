from model_bakery import baker
import json
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
from .mock_data import MockDB
from .invalid_mock_data import InvalidMockDB

# Load environment variables from .env file
load_dotenv()
SERVER = "http://testserver"
client = APIClient()


class HandleInboxTests(APITestCase):
    """
    Testing Remote Node Connectivity
    Running test Suite:
        python3 manage.py test api_tests.test_inbox.HandleInboxTests
    """
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        """
            Create mock data for testing. This mock data includes Data from other Teams, 
            has empty fields to test coverage for a variety of possible post requests.
            Examples: 
                Comments/Likes missing in 'Post' objects, or being set as empty lists/dictionaries.
                'Comment' objects having likes within them
                Objects containing pagination or without pagination
                Data fields being empty ( set to "")
                And more

            Mock Data Includes Data from Teams: Fushia, Honeydew (us), Chatreuse, Midnight Blue, Gold.
            Indentation of the JSON is off cause every team does it differently and id rather not manually fix it everytime
        """
        # Generate mock data
        self.MockDB = MockDB();
        self.InvalidMockDB = InvalidMockDB();

        # Generate mock data. Difference is this is an actual object in the database, 
        # whereas MockDB is a bunch of JSON objects ready to be converted into actual objects by sending to our inbox
        self.author = gen_author()
        self.inbox_url = f"{SERVER}/api/authors/{self.author.serial}/inbox" # //service/api/authors/{AUTHOR_SERIAL}/inbox

        # Default Username/Password to Access our API.
        self.AUTH_USERNAME = settings.AUTH_USERNAME
        self.AUTH_PASSWORD = settings.AUTH_PASSWORD

        self.valid_headers = {
            'Authorization': encode_basic_auth(self.AUTH_USERNAME, self.AUTH_PASSWORD)
        }

        self.invalid_headers = {
            'Authorization': encode_basic_auth(self.AUTH_USERNAME+'invalid', self.AUTH_PASSWORD+'invalid')
        }
        
        # Enable connections to this node
        Node.objects.create(
            host="testserver",
            our_username=self.AUTH_USERNAME,
            our_password=self.AUTH_PASSWORD,
            enable_connection=True
        )


    def test_inbox_post_request_with_authentication(self):
        """
        Test if POST requests to Inbox works WITH authentification
        """
        # Authentificate using invalid Username/Password
        # Send a POST request using invalid Username/Password
        post_data = {'type': ""}  # Data for the POST request
        response = self.client.post(self.inbox_url, data=post_data, **self.valid_headers)

        # POST request NOT be modified (type: "" is not supported. Must be "like", "post", etc.)
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_inbox_post_request_without_authentication(self):
        """
        Test if POST requests to Inbox works WITHOUT authentification
        """
        # Authentificate using invalid Username/Password
        # Send a POST request using invalid Username/Password
        post_data = {'some_key': 'some_value'}  # Data for the POST request
        response = self.client.post(self.inbox_url, data=post_data, **self.invalid_headers)

        # POST request should be UNsuccessful
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_inbox_author(self):
        """
        Test if our inbox can handle invalid Mock data inputs (JSON). (Request of type="author" should not modify anything) 
        """
        # For each Mock Object, run the test.
        mock_objects = self.MockDB.author_list
        for obj in mock_objects:

            # Send the author object into our Inbox
            response = self.client.post(self.inbox_url, data=json.dumps(obj), content_type="application/json", **self.valid_headers)
            
            # Nothing should be modified as our Inbox doesn't handle these kinds of objects
            self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_inbox_like(self):
        """
        Test if our inbox can handle our Mock data inputs (JSON). 
        """
        # For each Mock Object, run the test.
        mock_objects = self.MockDB.like_list
        for obj in mock_objects:

            # Create mock post to like in DB
            if not Post.objects.filter(fqid = obj.get("object")).exists():
                post = gen_post(fqid = obj.get("object"))
            response = self.client.post(self.inbox_url, data=json.dumps(PostSerializer(post).data), content_type="application/json", **self.valid_headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Send the Like object into our Inbox
            response = self.client.post(self.inbox_url, data=json.dumps(obj), content_type="application/json", **self.valid_headers)

            # POST request should be Successful
            self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

            # Like object should exist in the database
            fqid = obj.get("id")
            self.assertTrue(Like.objects.filter(fqid = fqid).exists())

    def test_inbox_follow(self):
        """
        Test if our inbox can handle our Mock data inputs (JSON). 
        """
        # For each Mock Object, run the test.
        mock_objects = self.MockDB.follow_list
        for obj in mock_objects:

            # Get FQIDs of Follower/Followed Authors
            followed_fqid = obj.get("object").get("id")
            follower_fqid = obj.get("actor").get("id")
            print("Followed: ", followed_fqid)
            print("Follower: ", follower_fqid)

            # Create Author to be Followed in DB
            if not Author.objects.filter(fqid = followed_fqid).exists():
                baker.make(Author, serial=100, fqid=followed_fqid, local=True)
            self.assertTrue(Author.objects.filter(fqid = followed_fqid).exists())

            # Create mock Author to Follow other Author in DB
            if not Author.objects.filter(fqid = follower_fqid).exists():
                baker.make(Author, serial=101, fqid=follower_fqid, local=True)
            self.assertTrue(Author.objects.filter(fqid = follower_fqid).exists())

            # Create follow request
            response = self.client.post(self.inbox_url, data=json.dumps(obj), content_type="application/json", **self.valid_headers)

            # Follow request should be Successful
            self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

    def test_inbox_comment(self):
        """
        Test if our inbox can handle our Mock data inputs (JSON). 
        """
        # For each Mock Object, run the test.
        mock_objects = self.MockDB.comment_list
        for obj in mock_objects:

            # Create mock post to comment in DB 
            if not Post.objects.filter(fqid = obj.get("post")).exists():
                post = gen_post(fqid = obj.get("post"))
            response = self.client.post(self.inbox_url, data=json.dumps(PostSerializer(post).data), content_type="application/json", **self.valid_headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Comment the post
            response = self.client.post(self.inbox_url, data=json.dumps(obj), content_type="application/json", **self.valid_headers)

            # POST request should be Successful
            self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

            # Comment object should exist in the database
            fqid = obj.get("id")
            self.assertTrue(Comment.objects.filter(fqid = fqid).exists())

    def test_inbox_post(self):
        """
        Test if our inbox can handle our Mock data inputs (JSON). 
        """
        # For each Mock Object, run the test.
        mock_objects = self.MockDB.post_list
        for obj in mock_objects:

            # Send the 'Post' Object into our Inbox
            response = self.client.post(self.inbox_url, data=json.dumps(obj), content_type="application/json", **self.valid_headers)

            # POST request should be Successful
            self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

            # Post object should exist in the database
            fqid = obj.get("id")
            self.assertTrue(Post.objects.filter(fqid = fqid).exists())


    def test_inbox_post_fail(self):
        """
        Test if our inbox can handle BAD Mock data inputs (JSON). 
        This mock test is design to make our Inbox Fail! And test if our Inbox handles bad data properly
        EX: Return 400 if missing FQID, etc.
        """
        # For each Mock Object, run the test.
        mock_objects = self.InvalidMockDB.post_list
        for obj in mock_objects:

            # Send the 'Post' Object into our Inbox
            response = self.client.post(self.inbox_url, data=json.dumps(obj), content_type="application/json", **self.valid_headers)

            # POST request should be Unsuccessful
            self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST])

            # Post object should not exist in the database
            fqid = obj.get("id")
            self.assertFalse(Post.objects.filter(fqid = fqid).exists())


    def test_inbox_like_fail(self):
        """
        Test if our inbox can handle BAD Mock data inputs (JSON). 
        This mock test is design to make our Inbox Fail! And test if our Inbox handles bad data properly
        EX: Return 400 if missing FQID, etc.
        """
        # For each Mock Object, run the test.
        mock_objects = self.InvalidMockDB.like_list
        for obj in mock_objects:

            # Create mock post to like in DB
            if not Post.objects.filter(fqid = obj.get("object")).exists():
                post = gen_post(fqid = obj.get("object"))
            response = self.client.post(self.inbox_url, data=json.dumps(PostSerializer(post).data), content_type="application/json", **self.valid_headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Send the Like object into our Inbox
            response = self.client.post(self.inbox_url, data=json.dumps(obj), content_type="application/json", **self.valid_headers)

            # POST request should be Unsuccessful
            self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST])

            # Like object should NOT exist in the database
            fqid = obj.get("id")
            self.assertFalse(Like.objects.filter(fqid = fqid).exists())

    def test_inbox_comment_fail(self):
        """
        Test if our inbox can handle BAD Mock data inputs (JSON). 
        This mock test is design to make our Inbox Fail! And test if our Inbox handles bad data properly
        EX: Return 400 if missing FQID, etc.
        """
        # For each Mock Object, run the test.
        mock_objects = self.InvalidMockDB.comment_list
        for obj in mock_objects:

            # Create mock post to comment in DB 
            if not Post.objects.filter(fqid = obj.get("post")).exists():
                post = gen_post(fqid = obj.get("post"))
            response = self.client.post(self.inbox_url, data=json.dumps(PostSerializer(post).data), content_type="application/json", **self.valid_headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Comment the post
            response = self.client.post(self.inbox_url, data=json.dumps(obj), content_type="application/json", **self.valid_headers)

            # POST request should be UNSuccessful
            self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST])

            # Comment object should NOT exist in the database
            fqid = obj.get("id")
            self.assertFalse(Comment.objects.filter(fqid = fqid).exists())

    def tearDown(self):
        Node.objects.all().delete()  
        LocalUser.objects.all().delete()
        Post.objects.all().delete()
        Author.objects.all().delete()
        Like.objects.all().delete
        Comment.objects.all().delete
        Follow.objects.all().delete
