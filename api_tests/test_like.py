import json
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

class HandleLikesTest(APITestCase):
    """
        Handles Testing for Like/Likes API.
    """
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        """ Initialize data for each test case within this class """
        # Create 2 Authors and 1 Post
        self.author = gen_author()
        self.other_author = gen_author()

        self.post = gen_post(self.author)
        self.other_post = gen_post(self.other_author)

        # Author likes their own post
        self.like1 = gen_like(self.author, self.post)
        # Another Author likes the same post
        self.like2 = gen_like(self.other_author, self.post)

        # author likes like 12 other posts for kicks
        # and also 12 people like other_author's post
        for i in range(12):
            gen_like(self.author)
            gen_like(post=self.other_post)

    """
        Test Function nomenclature: "test_<api function name>"
    """
    def test_get_post_likes(self):
        """
        Testing API Endpoint:
        http://{site}/api/authors/<author_serial>/posts/<post_serial>/likes
            where site is replaced by the host name.
        """
        url = f"{SERVER}/api/authors/{self.post.author.serial}/posts/{self.post.serial}/likes"
        response = client.get(url)
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()

        # Test response data matches API specs
        assert data['type'] == "likes", f"Recieved: {data['type']}"
        assert data['count'] == 1, f"Recieved: {data}"  # Only 1 Author, Other than the Post's Author, Liked this post.
        assert len(data['src']) == data['count'],\
            f"{len(data['src'])} != {data['count']}"  # Ensure Number of Likes is Consistent in the response

    def test_get_post_likes_404(self):
        """
        Test 404 Responses if Author/Post does not exist in the database

        Testing API Endpoint:
            http://{site}/api/authors/<author_serial>/posts/<post_serial>/all_likes
            where site is replaced by the host name.
        """
        # Test 404 response when Author does not exist
        url = f"{SERVER}/api/authors/{999}/posts/{self.post.serial}/likes"
        response = client.get(url)
        assert response.status_code == 404, f"Recieved: {response.status_code}"

        # Test 404 response when Post does not exist
        url = f"{SERVER}/api/authors/{self.post.author.serial}/posts/{999}/likes"
        response = client.get(url)
        assert response.status_code == 404, f"Recieved: {response.status_code}"

    def test_get_post_all_likes(self):
        """
        Testing API Endpoint:
            http://{site}/api/authors/<author_serial>/posts/<post_serial>/all_likes
            where site is replaced by the host name.
        """
        url = f"{SERVER}/api/authors/all_likes"
        data = { "type": "like", "author_fqid": self.author.fqid, "post_fqid": self.post.fqid }

        response = client.post(url, data=json.dumps(data), content_type="application/json")
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()

        # Test response data matches API specs
        assert data['type'] == "likes", f"Recieved: {data['type']}"
        assert data['count'] == 2, f"Recieved: {data['count']}"  # Should Get ALL Likes to this particular post, without Filtering.
        assert len(data['src']) == 2, f"Recieved: {len(data['src'])}"  # Ensure Number of Likes is Consistent in the response


    def test_get_post_all_likes_404(self):
        """
        Test 404 Responses if Author/Post does not exist in the database

        Testing API Endpoint:
            http://{site}/api/authors/<author_serial>/posts/<post_serial>/all_likes
            where site is replaced by the host name.
        """
        # Test 404 response when Author does not exist
        url = f"{SERVER}/api/authors/{999}/posts/{self.post.serial}/all_likes"
        response = client.get(url)
        assert response.status_code == 404, f"Recieved: {response.status_code}"

        # Test 404 response when Post does not exist
        url = f"{SERVER}/api/authors/{self.post.author.serial}/posts/{999}/all_likes"
        response = client.get(url)
        assert response.status_code == 404, f"Recieved: {response.status_code}"

    def test_get_fqid_post_likes(self):
        """
        Testing API Endpoint:
            http://{site}/api/posts/<fqid>/likes
            where site is replaced by the host name.
        """
        url = f"{SERVER}/api/posts/{self.post.fqid}/likes"
        response = client.get(url)
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()

        # Test response data matches API specs
        assert data['type'] == "likes", f"Recieved: {data['type']}"
        assert data['count'] == 1, f"Recieved: {data['count']}"  # Should Get ALL Likes to this particular post, without Filtering.
        assert len(data['src']) == 1, f"Recieved: {len(data['src'])}"  # Ensure Number of Likes is Consistent in the response

    def test_get_fqid_post_likes_404(self):
        """
        Test 404 Responses if POST FQID does not exist in the database

        Testing API Endpoint:
            http://{site}/api/posts/<fqid>/likes
            where site is replaced by the host name.
        """
        # Test 404 response when POST FQID does not exist
        url = f"{SERVER}/api/posts/{999}/likes" # FQID is a URL
        response = client.get(url)
        assert response.status_code == 404, f"Recieved: {response.status_code}"

    def test_get_like(self):
        """
        Testing API Endpoint:
            http://{site}/api/liked/<path:like_fqid>
            where site is replaced by the host name.
        """
        url = f"{SERVER}/api/liked/{self.like1.fqid}"
        response = client.get(url)
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()

        # Test response data matches API specs
        assert data['type'] == "like", f"Recieved: {data['type']}"
        assert data['id'] == self.like1.fqid, f"Recieved: {data['id']}"    # Ensure the correct Like object is returned
        assert data['object'] == self.post.fqid, f"Recieved: {data['object']}" # Ensure the correct Post object FQID is returned

    def test_get_like_404(self):
        """
        Test 404 Responses if LIKE FQID does not exist in the database

        Testing API Endpoint:
            http://{site}/api/liked/<path:like_fqid>
            where site is replaced by the host name.
        """

        # Test 404 response when POST FQID does not exist
        url = f"{SERVER}/api/liked/{999}"
        response = client.get(url)
        assert response.status_code == 404, f"Recieved: {response.status_code}"

    def tearDown(self):
        # Default tearDown crashes here
        # Just kill authors because of CASCADE rules
        Author.objects.all().delete()
