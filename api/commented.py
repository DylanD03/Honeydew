from urllib.parse import unquote

from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import CommentSerializer
from honeydew.models import Author, Comment


HTTP = "https://"
SITE = Site.objects.get_current


@api_view(['GET', 'POST'])
def handle_author_commented(request, pk):

    # Get requester
    requester = "\\\\\\\\"
    if request.user.is_authenticated:
        requester = request.user.author.fqid

    if request.method == "GET":
        # Get author
        comments = Comment.objects.filter(  # ~Q(post__visibility=Post.DELETED),
                                          author__serial=pk)\
                                  .order_by("-published")
        # Get page size and number
        page = int(request.GET.get('page', 1))  # Default first page
        size = int(request.GET.get('size', 5))  # Default size 5

        # Pagination stuff
        paginate = PageNumberPagination()
        paginate.page = page
        paginate.page_size = size
        paginated_comments = paginate.paginate_queryset(comments, request)

        # Serialize and send data
        # NOTE Does not return a `comments` object as per the spec
        serializer = CommentSerializer(paginated_comments, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        author = get_object_or_404(Author, serial=pk)
        requestor_fqid = request.user.author.fqid

        if author.fqid == requestor_fqid:

            serializer = CommentSerializer(request.data)

            if not serializer.is_valid():
                return Response(status=400, data=serializer.errors)

            serializer.save()
            return Response(status=201, data=serializer.data)
        else:
            return Response(status=401,
                            data="You do not own this account")


@api_view(['GET'])
def get_fqid_author_commented(request, fqid):
    # Percent Decode fqid
    fqid = unquote(fqid)
    # Get comments with matching author
    comments = Comment.objects.filter(author=fqid).order_by("-published")

    # Get page size and number
    page = int(request.GET.get('page', 1))  # Default first page
    size = int(request.GET.get('size', 5))  # Default size 5

    # Pagination stuff
    paginate = PageNumberPagination()
    paginate.page = page
    paginate.page_size = size
    paginated_comments = paginate.paginate_queryset(comments, request)

    # Serialize and send data
    # NOTE Does not return a `comments` object as per the spec
    serializer = CommentSerializer(paginated_comments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_author_commented(request, author_serial, comment_serial):
    # Get comment
    comment = get_object_or_404(Comment,
                                author__serial=author_serial,
                                serial=comment_serial)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)


@api_view(['GET'])
def get_commented(request, fqid):
    # Percent Decode fqid
    fqid = unquote(fqid)
    comment = get_object_or_404(Comment, fqid=fqid)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)
