from urllib.parse import unquote

from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import FollowersSerializer
from honeydew.models import Author, Follow


HTTP = "https://"
SITE = Site.objects.get_current


@api_view(['GET'])
def get_followers(request, pk):
    print("In get_followers")

    # Get matching follow objects
    follows = Follow.objects.filter(following__serial=pk).order_by("-follower__fqid")

    # Get page number and size
    size = int(request.GET.get('size', '5'))
    page = (int(request.GET.get('page', '1')))

    # Retrieve follows
    paginate = PageNumberPagination()
    paginate.page = page
    paginate.page_size = size
    paginated_follows = paginate.paginate_queryset(follows, request)

    followers \
        = [i.follower for i in paginated_follows]

    data = {
        "type": "followers",
        "followers": followers
    }
    serializer = FollowersSerializer(data)

    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def handle_follower(request, author_serial, foreign_author_fqid):
    """
    GET:
        Returns 200 if "foreign_author" is a follower of "author"

    PUT:
        Returns 201 when it successfully adds "foreign_author" as an follower of
        "author"

    DELETE:
        Returns 200 when it successfully removes "foreign_author"
        from the followers of "author"
    """
    # Authenticating Put/DELETE early for readability
    if request.method in ['PUT', 'DELETE']:
        owner = None
        if request.user.is_authenticated:
            owner = (author_serial == request.user.author.serial)
        if not owner:
            return Response(status=403)

    # Percent Decode FQID
    foreign_author_fqid = unquote(foreign_author_fqid)
    if request.method == "GET":
        # If follower exists, return 200 OKAY
        # Otherwise, return 404
        follow = get_object_or_404(Follow,
                                   follower__fqid=foreign_author_fqid,
                                   following__serial=author_serial)
        return Response(status=200)
    elif request.method == "PUT":
        # SANITY CHECK:
        # Follower -> following
        # ('Follower' is following 'following')
        author = get_object_or_404(Author, serial=author_serial)
        follower = get_object_or_404(Author, fqid=foreign_author_fqid)
        Follow.objects.create(following=author,
                              follower__fqid=follower)
        return Response(status=201)
    elif request.method == "DELETE":
        follow = get_object_or_404(Follow,
                                   following__serial=author_serial,
                                   follower__fqid=foreign_author_fqid)
        follow.delete()
        return Response(status=200)
    else:
        return Response(status=405)
