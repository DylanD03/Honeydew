from urllib.parse import unquote

from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import AuthorSerializer, AuthorsSerializer
from honeydew.models import Author


HTTP = "https://"
SITE = Site.objects.get_current


@api_view(['GET'])
def get_authors(request):
    print("**** in API get_authors *****")
    # query handling
    size = int(request.GET.get('size', '5'))
    page = (int(request.GET.get('page', '1')))

    # Get relevant authors
    authors = Author.objects.all().filter(local=True) #.order_by("serial")

    # Page authors
    paginate = PageNumberPagination()
    paginate.page = page
    paginate.page_size = size
    paginated_authors = paginate.paginate_queryset(authors, request)

    # Serializing data
    data = {
        "type": "authors",
        "authors": paginated_authors
    }
    authors_serializer = AuthorsSerializer(data)

    return Response(authors_serializer.data)


@api_view(['GET', 'PUT'])
def handle_author(request, pk):
    """
    API View that handles returning or editting an existing Author based on
    the URL.
    """
    # Get a specific author
    if request.method == "GET":
        author = get_object_or_404(Author, serial=pk)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    # Modify author stuff
    elif request.method == "PUT":
        author = get_object_or_404(Author, serial=pk)

        if request.user.author == author:
            serializer = AuthorSerializer(author,
                                          data=request.data,
                                          partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200, data=serializer.data)
            return Response(status=400, data=serializer.errors)
        else:
            return Response(status=401,
                            data="Cannot modify other Authors profile")

    else:
        return Response(status=405)


@api_view(['GET'])
def get_fqid_author(request, fqid):
    """
    GET [local]: retrieve AUTHOR_FQID's profile
    """
    fqid = unquote(fqid)
    # NOTE Should this reference our copy???
    # Probably, the API seems Push-only with no pulls
    author = get_object_or_404(Author, fqid=fqid)
    serializer = AuthorSerializer(author)
    return Response(serializer.data)
