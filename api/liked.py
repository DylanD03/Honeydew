from urllib.parse import unquote

from django.contrib.sites.models import Site
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import LikeSerializer
from honeydew.models import Like


HTTP = "https://"
SITE = Site.objects.get_current



@api_view(['GET'])
def get_author_liked(request, author_serial):
    """
        Retrieve a paginated list of Likes objects by the given author (author_serial).
        Ordered by date, where most recent like objects appear first

        Example usage of pagination queries: ?page=4&size=40
        Full Example usage:
            http://{site}/api/authors/<author_serial>/liked
            where site is replaced by the host name.

        "Things Liked By Author"
        GET [local, remote] a list of likes by AUTHOR_SERIAL

        url: 'authors/<str:author_serial>/liked'
    """
    # Get Query Parameters from request. 1 Based Indexing
    # Ex: ?page=4&size=40
    page = int(request.GET.get('page', 1))  # Default first page
    size = int(request.GET.get('size', 5))  # Default size 5

    # Query all like objects corresponding to the given author
    likes = Like.objects.filter(author__serial=author_serial).order_by('-published')
    total_likes = likes.count()

    # Apply pagination: https://www.django-rest-framework.org/api-guide/pagination/#pagenumberpagination
    paginate = PageNumberPagination()
    paginate.page = page
    paginate.page_size = size
    paginated_likes = paginate.paginate_queryset(likes, request)

    # # Create a list of likes (src)
    src = LikeSerializer(paginated_likes, many=True)

    # # Format the response data
    response_data = {
        "type": "likes",
        "page": "", # List of likes by author in all posts
        "id": "",   # List of likes by author in all posts
        "page_number": page,
        "size": size,
        "count": total_likes,
        "src": src.data
    }

    return Response(response_data, status=200)


@api_view(['GET'])
def get_author_all_liked(request, author_serial):
    """
        Extra API function not required by Project specifications.
        Returns all likes that a particular author has made

        "Things Liked By Author"
        GET [local, remote] a list of likes by AUTHOR_SERIAL

        Full Example usage:
            http://{site}/api/authors/<str:author_serial>/all_liked
            where site is replaced by the host name.

        - Difference between this and get_author_liked, is that this function
           does not do pagination, thereby loading ALL likes from a particular author.

        URL Inputs:
            (String) author_serial: Example: "1"

        Output: Likes Object in JSON format
    """
    # Query all like objects corresponding to the given author
    likes = Like.objects.filter(author__serial=author_serial).order_by('-published')
    total_likes = likes.count()

    # Create a list of likes (src)
    src = LikeSerializer(likes, many=True)

    # Format the response data
    response_data = {
        "type": "likes",
        "page": "", # List of likes by author in all posts
        "id": "",   # List of likes by author in all posts
        "page_number": 1,
        "size": total_likes,
        "count": total_likes,
        "src": src.data
    }

    return Response(response_data, status=200)


@api_view(['GET'])
def get_author_like(request, author_serial, like_serial):
    """
        GET [local, remote] a single like
    """
    like = Like.objects.get(author__serial=author_serial, serial=like_serial)
    serializer = LikeSerializer(like)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_fqid_author_liked(request, author_fqid):
    """
        Retrieve a paginated list of Like objects by the given author (author_serial).
        Ordered by date, where most recent like objects appear first

        Things Liked By Author
        GET [local] a list of likes by AUTHOR_FQID

        Full Example usage:
            http://{site}/api/authors/<str:author_fqid>/liked/
            where site is replaced by the host name.

        URL Inputs:
            (String) author_fqid: Example: "http://nodeaaaa/api/authors/111"

        Output: Likes Object in JSON format
    """
    # Percent Decode fqid
    author_fqid = unquote(author_fqid)
    # Get relevant likes
    likes = Like.objects.filter(author=author_fqid).order_by("-published")

    # Get Query Parameters from request. 1 Based Indexing
    # Ex: ?page=4&size=40
    page = int(request.GET.get('page', 1))  # Default first page
    size = int(request.GET.get('size', 5))  # Default size 5

    # Apply pagination: https://www.django-rest-framework.org/api-guide/pagination/#pagenumberpagination
    paginate = PageNumberPagination()
    paginate.page = page
    paginate.page_size = size
    paginated_likes = paginate.paginate_queryset(likes, request)

    # # Create a list of likes (src)
    src = LikeSerializer(paginated_likes, many=True)

    # # Format the response data
    response_data = {
        "type": "likes",
        "page": "", # List of likes by author in all posts
        "id": "", # Isn't saved in db
        "page_number": page,
        "size": size,
        "count": likes.count(),
        "src": src.data
    }

    return Response(response_data, status=200)
