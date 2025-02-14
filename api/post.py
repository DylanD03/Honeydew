from urllib.parse import unquote

from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .authentication import get_owner_friend
from .serializers import PostSerializer, PostsSerializer
from honeydew.models import Author, Post


HTTP = "https://"
SITE = Site.objects.get_current


@api_view(['GET', 'PUT', 'DELETE'])
def handle_post(request, author_serial, post_serial):
    # Delete/Put Requests must be Authenticated

    author = get_object_or_404(Author, serial=author_serial)
    owner, friend = get_owner_friend(request, author)

    # Friends Posts must be Authenticated
    post = get_object_or_404(Post, author__serial=author_serial, serial=post_serial)
    # Pretend deleted posts don't exist
    if (post.visibility == Post.DELETED):
        return Response(status=404)

    if request.method == "GET":

        if (owner or friend or post.visibility == Post.PUBLIC):
            serializer = PostSerializer(post)
            return Response(status=200, data=serializer.data)
        else:
            return Response(status=401)

    # Anyone besides the owner should be rejected at this point
    if not owner:
        return Response(status=401)

    if request.method == "PUT":
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data=serializer.data)
        return Response(status=400, data=serializer.errors)

    if request.method == "DELETE":
        post.visibility = Post.DELETED
        post.save()
        return Response(status=200)

    return request(status=405)


@api_view(['GET'])
def get_fqid_post(request, fqid):

    # Get a post via FQID
    fqid = unquote(fqid)
    post = get_object_or_404(Post, fqid=fqid)
    owner, friend = get_owner_friend(request, post.author)

    # friends posts: must be authenticated
    if (post.visibility == Post.FRIENDS and not (owner or friend)):
        return Response(status=401)

    # Pretend deleted posts don't exist
    if (post.visibility == Post.DELETED):
        return Response(status=404)

    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def handle_author_posts(request, pk):
    # Grab author to get fqid for post foreign key
    author = get_object_or_404(Author, serial=pk)
    mine, friend = get_owner_friend(request, author)

    if request.method == 'GET':

        # Handle query for pages
        page = int(request.GET.get('page', 1))  # Default first page
        size = int(request.GET.get('size', 5))  # Default size 5

        if friend or mine:  # access to all posts but deleted
            posts = Post.objects.filter(author__serial=pk)\
                                .order_by("-published")\
                                .exclude(visibility="DELETED")
        else:  # only view public posts
            posts = Post.objects.filter(author__serial=pk, visibility = "PUBLIC")\
                            .order_by("-published")

        #i =0
        #for post in posts:
           #print(f"{i}.", post.description)
            #i += 1
        # Page stuff
        paginate = PageNumberPagination()
        paginate.page = page
        paginate.page_size = size
        paginated_posts = paginate.paginate_queryset(posts, request)

        #for page in paginated_posts:
            #print(page.fqid)

        # Serializing data
        data = {
            "type": "posts",
            "page_number": page,
            "size": size,
            "count": posts.count(),
            "src": paginated_posts
        }
        serializer = PostsSerializer(data)
        return Response(status=200, data=serializer.data)

    elif request.method == 'POST':
        # NOTE Document!!!!!

        if mine:
            new_post_data = {
                # Not included: id, page, comments, likes, published
                "author": author,
                "title": request.data.get("title"),
                "description": request.data.get("description"),
                "content": request.data.get("content"),
                "contentType": request.data.get("contentType"),
                "visibility": request.data.get("visibility"),
            }
            serializer = PostSerializer(new_post_data)
            if serializer.is_valid():
                serializer.save()
                return Response()
            return Response(status=400, data=serializer.errors)
        else:
            return Response(status=401)
