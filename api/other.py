from django.contrib.sites.models import Site
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from api.inbox import push_to_followers, push_to_friends, push_to_owner
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .serializers import PostSerializer, LikeSerializer
from honeydew.models import Author, Like, Post

import json
HTTP = "https://"
SITE = Site.objects.get_current


@api_view(['POST'])
def has_user_liked_post(request):
    """
        Checks if the user corresponding user_serial has liked a specific post, post_serial,
        made by author_serial.


        Full Example usage:
            http://{site}/api/user/<int:user_serial>/authors/<int:author_serial>/posts/<int:post_serial>/has_liked
            where site is replaced by the host name.

        URL Inputs:
            (url) user_serial: Example: 
            (url) post_serial: Example: 
            (url) author_serial: Example: 

        Output: A JSON response indicating whether the user has liked the post.
        Example Return:
            response = {
                'is_liked': True
            }
    """
    body_data = json.loads(request.body)
    print("****has_user_liked_post****")
    # Get the user and the post from the database
    print("user fqid: ", body_data.get('user_fqid'))
    user = get_object_or_404(Author, fqid=body_data.get('user_fqid'))
    print("found user")

    post = get_object_or_404(Post, author__fqid=body_data.get('author_fqid'), fqid=body_data.get('post_fqid'))
    print("found post   ")

    # Check if a Like object exists for this user and post
    is_liked = Like.objects.filter(author=user, post=post).exists()
    print("IS_LIKED:", is_liked)
    return Response({'is_liked': is_liked}, status=200)


@api_view(['DELETE'])
def user_unlike_post(request):
    """
    Deletes a Like Object, to indicate that a User has unliked the author's post.

    Full Example usage:
        http://{site}/api/user/<int:user_serial>/authors/<int:author_serial>/posts/<int:post_serial>/unlike_post
        where site is replaced by the host name.

    URL Inputs:
        (String) user_serial: Example: "1"
        (String) post_serial: Example: "1"
        (String) author_serial: Example: "1"

    Output: A JSON response indicating whether the like has been deleted.
    Example Return:
        response = {
            'message': 'Like deleted successfully'
        }
    """
    print("*** user_unlike_post ***")
    if request.method == 'DELETE':
        try:
            body_data = json.loads(request.body)
            like = Like.objects.get(author__fqid=body_data.get('user_fqid'), post__author__fqid=body_data.get('author_fqid'), post__fqid=body_data.get('post_fqid'))
            like.delete()
            return Response({"message": "Like deleted successfully"}, status=200)
        except Like.DoesNotExist:
            return Response({"error": "Like not found"}, status=404)
        except Exception as e:
            print("error:", str(e))
            return Response({"error": str(e)}, status=500)


@api_view(['POST'])
def handle_author_github_posts(request, pk):
    """
    Deletes a Like Object, to indicate that a User has unliked the author's post.

    Parameters:
    - user_serial: The serial number of the user
    - post_serial: The serial number of the post
    - author_serial: The serial number of the author who made the post

    Returns:
    - String indicating success or error
    """
    print(" *** in handle_author_github_posts ***")
    author = get_object_or_404(Author, serial=pk)
    print("author: ", author)

    try:
        # Check to see if the post already exists in the database
        # We check by comparing github activity id, which should be unique for each github activity
        postExists = Post.objects.filter(github_activity_id=request.data.get("github_activity_id")).exists()
        print("postExists:", postExists)
        if postExists:
            return Response({"message": "Post already exists."}, status=204)

        # Create and save the Post object into our database
        post = Post.objects.create(
            author=author,
            title=request.data.get("title"),
            description=request.data.get("description"),
            content_type=request.data.get("content_type"),
            content=request.data.get("content"),
            visibility=request.data.get("visibility"),
            github_activity_id=request.data.get("github_activity_id"),
        )
        post.save()
        print("Post Saved")

        # Send this new post to all Nodes connected to this Node.
        try:
            serializer = PostSerializer(post)
            if post.visibility == Post.FRIENDS:
                print("pushing to Friends")
                push_to_friends(serializer, author)
            else:
                print("pushing to Followers")
                push_to_followers(serializer, author)
        except:
            print("cannot propogate github post")

        return Response(200)

    except Exception as e:
        print("Post did not save: ", str(e))
        return Response({"error": str(e)}, status=400)



class SharePostView(APIView):
    
    """
    API view for sharing a post. This allows users to share an existing post with additional comments.
    """
    
    def post(self, request, fqid):
        
        # Get the user's comment for sharing
        user_comment = request.data.get('shareComment', '')
        author_fqid = request.POST.get('fqid')
        author_obj = get_object_or_404(Author, fqid=author_fqid)
        current_author = author_obj.display_name

        # Retrieve the original post
        original_post = get_object_or_404(Post, fqid=fqid)
        serializer = PostSerializer(original_post)

        # Generate URLs for the original post and author's profile
        original_post_url = reverse("view_post", kwargs={"id": original_post.fqid})
        author_profile_url = reverse("view_author_profile", kwargs={"author_id": original_post.author.fqid})

        # Ensure the original post is public
        if original_post.visibility != 'PUBLIC':
            raise PermissionDenied("This post cannot be shared as it is not public.")

        # Construct the shared post content
        content_with_mention = (
            f"<a href=\"{author_profile_url}\" onclick=\"userLinkProfile('{original_post.author.display_name}');\">@{original_post.author.display_name}</a>: {original_post.title} "
            f"{original_post.content}"
            f"<p>(View original post: <a href=\"{original_post_url}\">here</a>)</p>"
        )
        repost_title = f"Repost: {original_post.title}"

        # Create a new shared post
        new_post = Post.objects.create(
            author=author_obj,
            title=repost_title,
            content_type=Post.MARK,
            description=user_comment,
            visibility="PUBLIC",
            content=content_with_mention,
            shared_post=original_post,
        )

        # Send this new post to all Nodes connected to this Node.
        serializer = PostSerializer(new_post)
        if new_post.visibility == Post.FRIENDS:
            push_to_friends(serializer, author_obj)
        else:
            push_to_followers(serializer, author_obj)
            
        return redirect('stream-home')
