from django.urls import include, path
from dotenv import load_dotenv
from rest_framework.test import APITestCase, APIClient

from .model_gen import gen_author, gen_user, gen_follow
from honeydew.models import LocalUser, Author, Post, Friendship
from django.db.models import Q

# Load environment variables from .env file
load_dotenv()
SERVER = "https://testserver"
client = APIClient()


class HandleFollowerTest(APITestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):

        # Single author relationship for testing
        self.user = gen_user()
        self.author2 = gen_author()
        gen_follow(self.author2, self.user.author)  # author2 follows author

        # author follows 5 other authors
        for i in range(5):
            a = gen_author()
            gen_follow(self.user.author, a)

        # author2 has 5 followers
        for i in range(5):
            gen_follow(gen_author(), self.author2)

        # Unrelated author for making a request later
        self.author3 = gen_author()

    def test_follower_get(self):
        response = client.get(f"{SERVER}/api/authors/1/followers")
        assert response.status_code == 200, f"Recieved: {response.status_code}"
        data = response.json()

        data = response.json()
        assert data['type'] == "followers", f"Recieved: {data['type']}"
        assert len(data['followers']) == 1, f"Recieved: {len(data['followers'])}, {self.user.author.serial}"


    def test_handle_follower(self):
        response = client.get(f"{SERVER}/api/authors/1/followers/{self.author2.fqid}")
        assert response.status_code == 200, f"Recieved: {response.status_code}"

        response2 = client.put(f"{SERVER}/api/authors/1/followers/{self.author2.fqid}")
        assert response2.status_code == 403, f"Recieved: {response2.status_code}"

        response3 = client.delete(f"{SERVER}/api/authors/3/followers/1")
        assert response3.status_code == 403,\
            f"Recieved: {response3.status_code}"

        # assert client.login(username=self.username, password=self.password),\
        #     "Login failed for some reason"
        client.force_authenticate(user=self.user)
        response = client.delete(f"/api/authors/1/followers/{self.author2.fqid}")
        # NOTE Doesn't check if it was actually deleted
        assert response.status_code == 200,\
            f"Recieved: {response.status_code}"

        # author3 is not a follower of author 1, so it should result in a 404. 
        response4 = client.get(f"{SERVER}/api/authors/1/followers/{self.author3.fqid}")
        assert response4.status_code == 404, f"Recieved: {response4.status_code}"

        #author3 now follows author 1, so it should now result in a 200.
        gen_follow(self.author3, self.user.author)
        response5 = client.get(f"{SERVER}/api/authors/1/followers/{self.author3.fqid}")
        assert response5.status_code == 200, f"Recieved: {response5.status_code}"
        
        # Delete follow.
        response = client.delete(f"/api/authors/1/followers/{self.author3.fqid}")
        assert response.status_code == 200, f"Recieved: {response.status_code}"

        # Delete follow. Since we already deleted, cannot delete again. 404 as follow does not exist.
        response = client.delete(f"/api/authors/1/followers/{self.author3.fqid}")
        assert response.status_code == 404, f"Recieved: {response.status_code}"

        # Checking Friends relationship. Friends relationship does not have an API. Can replace if we create an API.
        # No friendship between author1 and author3 right now.
        author_friendships = Friendship.objects.filter(Q(author1=self.user.author) | Q(author2=self.user.author))
        friendship = author_friendships.filter(Q(author1=self.author3) | Q(author2=self.author3))
        assert len(friendship) == 0, f"Received: {len(friendship)} friendship."
        # Author1 and author3 follow each other - creating a friendship.
        gen_follow(self.author3, self.user.author)
        gen_follow(self.user.author, self.author3)

        # check if friendship was created.
        author_friendships = Friendship.objects.filter(Q(author1=self.user.author) | Q(author2=self.user.author))
        friendship = author_friendships.filter(Q(author1=self.author3) | Q(author2=self.author3))
        assert len(friendship) == 1, f"Received: {len(friendship)} friendship."
        
        # Resetting Authentication in case it messes with use later <3
        # Alternatively, make a client every time,
        # but I don't feel like refactoring
        client.force_authenticate(user=None)

    def tearDown(self):
        LocalUser.objects.all().delete()
        Author.objects.all().delete()
        Post.objects.all().delete()
