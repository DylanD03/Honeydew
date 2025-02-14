from urllib.parse import unquote

from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import CommentSerializer, CommentsSerializer
from honeydew.models import Comment, Post
from stream.views import friends_list


HTTP = "https://"
SITE = Site.objects.get_current


@api_view(['GET'])
def get_post_comments(request, author_serial, post_serial):
    # Get the paged comments of a specific post
    post = get_object_or_404(Post,
                             serial=post_serial,
                             author__serial=author_serial)

    if post.visibility == "FRIENDS":
        post_author_fqid = post.author_id
        post_author_friends = friends_list(post_author_fqid)
        if request.user.author.fqid not in post_author_friends:
            # requestor is not a friend of post author
            return Response(status=401)

    # Get comments that the author has written
    comments = Comment.objects.filter(post=post.fqid)\
                              .order_by("-published")
    # Get page size and number
    page = int(request.GET.get('page', 1))  # Default first page
    size = int(request.GET.get('size', 5))  # Default size 5

    # Pagination stuff
    paginate = PageNumberPagination()
    paginate.page = page
    paginate.page_size = size
    paginated_comments = paginate.paginate_queryset(comments, request)

    # Prepare data for serializer
    data = {
        "id": f"{post.fqid}/comments",
        "page": f"{HTTP}{SITE().domain}/authors/{author_serial}/posts/{post_serial}",
        "page_number": page,
        "size": size,
        "count": comments.count(),
        "src": paginated_comments
    }
    # Serialize and send data
    serializer = CommentsSerializer(data)
    return Response(serializer.data)


@api_view(['GET'])
def get_fqid_post_comments(request, fqid):

    # Percent Decode fqid
    fqid = unquote(fqid)
    # Get post by fqid
    post = get_object_or_404(Post, fqid=fqid)

    if post.visibility == "FRIENDS":
        post_author_fqid = post.author_id
        post_author_friends = friends_list(post_author_fqid)
        if request.user.author.fqid not in post_author_friends:
            # requestor is not a friend of post author and
            # cannot see comments on post
            return Response(status=401)

    # Get commends on post
    comments = Comment.objects.filter(post=post.fqid)\
                              .order_by("-published")
    # Get page size and number
    page = int(request.GET.get('page', 1))  # Default first page
    size = int(request.GET.get('size', 5))  # Default size 5

    # Pagination stuff
    paginate = PageNumberPagination()
    paginate.page = page
    paginate.page_size = size
    paginated_comments = paginate.paginate_queryset(comments, request)

    # Prep data for serializer
    data = {
        "id": f"{post.fqid}/comments",
        "page": "TODO part 3, store pages in models",
        "page_number": page,
        "size": size,
        "count": comments.count(),
        "src": paginated_comments
    }
    # Serialize and send data
    serializer = CommentsSerializer(data)
    return Response(serializer.data)


@api_view(['GET'])
def get_specific_comment(request, author_serial, post_serial, comment_fqid):
    # Percent Decode fqid
    comment_fqid = unquote(comment_fqid)
    # get relevant comment
    comment = get_object_or_404(Comment, fqid=comment_fqid)

    # TODO check if the author/post match?

    # Serialize and send data
    serializer = CommentSerializer(comment)
    return Response(serializer.data)


@api_view(['GET'])
def get_fqid_comment(request, fqid):
    # Percent Decode fqid
    fqid = unquote(fqid)
    # get relevant comment
    comment = get_object_or_404(Comment, fqid=fqid)

    # Serialize and send data
    serializer = CommentSerializer(comment)
    return Response(serializer.data)


@api_view(['GET'])
def get_post_all_comments(request, author_serial, post_serial):
    """
        GET [local, remote] a list of comments from ALL authors on AUTHOR_SERIAL's post POST_SERIAL
        /api/authors/<int:author_serial>/posts/<int:post_serial>/all_comments

                                    Extra API function.
        - This function also does not do pagination, thereby loading ALL comments for a particular posts.

        Inputs:
            author_serial is the author who made the post.
            post_serial is the post being commented on

        Returns:
            comments object

        author_serial is the author who made the post.
    """
    # Get post object
    post = get_object_or_404(Post,
                             author__serial=author_serial,
                             serial=post_serial)

    if post.visibility == "FRIENDS":
        post_author_fqid = post.author_id
        post_author_friends = friends_list(post_author_fqid)
        if request.user.author.fqid not in post_author_friends:
            return Response(status=401) #requestor is not a friend of post author and therefore cannot see comments on post

    # Query all like objects corresponding to the all other authors
    comments = Comment.objects.filter(post=post).order_by('-published')
    comments_total = comments.count()

    # Create a list of likes (src)
    src = CommentSerializer(comments, many=True)

    # Format the response data into a "Likes" object
    response_data = {
        "type": "likes",
        "page": post.fqid,
        "id": f"{post.fqid}/comments",
        "page_number": 1,
        "size": comments_total,
        "count": comments_total,
        "src": src.data
    }

    return Response(response_data, status=200)
