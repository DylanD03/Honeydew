import base64
from urllib.parse import unquote

from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.authentication import CustomAuthentication
from honeydew.models import Author, Post
from stream.views import friends_list


HTTP = "https://"
SITE = Site.objects.get_current


@api_view(['GET'])
# @authentication_classes([CustomAuthentication])  # Apply custom authentication here
# @permission_classes([IsAuthenticated])
def get_image(request, author_serial, post_serial):

    author = get_object_or_404(Author, serial=author_serial)
    friend_or_owner = False
    if request.user.is_authenticated:
        if request.user.author in friends_list(author.fqid):
            friend_or_owner = True
        elif request.user.author == author:
            friend_or_owner = True

    post = get_object_or_404(Post,
                             author__serial=author_serial,
                             serial=post_serial)

    if post.visibility == Post.DELETED:
        return Response(status=404)

    if post.content_type != Post.IMAGE:
        # No image is found at endpoint
        return Response(status=405)

    if not friend_or_owner and post.visibility == Post.FRIENDS:
        return Response(status=403)

    image = post.content
    encoded = base64.b64encode(image)

    return Response(status=200, data=encoded, content_type="image/png;base64")


@api_view(['GET'])
# @authentication_classes([CustomAuthentication])  # Apply custom authentication here
# @permission_classes([IsAuthenticated])
def get_fqid_image(request, post_fqid):
    post_fqid = unquote(post_fqid)
    post = get_object_or_404(Post, fqid=post_fqid)

    friend_or_owner = False
    if request.user.is_authenticated:
        if request.user.author in friends_list(post.author.fqid):
            friend_or_owner = True
        elif request.user.author == post.author:
            friend_or_owner = True

    if post.visibility == Post.DELETED:
        return Response(status=404)

    if post.content_type != Post.IMAGE:
        # No image is found at endpoint
        return Response(status=405)

    if not friend_or_owner and post.visibility == Post.FRIENDS:
        return Response(status=403)

    image = post.content
    encoded = base64.b64encode(image)

    return Response(status=200, data=encoded, content_type="image/png;base64")
