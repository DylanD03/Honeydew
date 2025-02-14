from django.urls import path

from . import authentication, inbox, author, comment, commented, \
    follow, image, like, liked, other, post


# urlpatterns contains all of the routes that this application supports routing for.
# this routes traffic from polls/ to the index function that we defined earlier in the views file.
#
# HACK fqids are represented with `path` it feels a bit dirty though
# TODO Better names?
app_name = "polls"
urlpatterns = [
    # Authors API
    # GET
    path('authors/',
         author.get_authors,
         name='get_authors'),

    # Single Author API
    # GET / PUT
    path('authors/<int:pk>',
         author.handle_author,
         name='get_author_serial'),

    # Followers API
    # GET
    path('authors/<int:pk>/followers',
         follow.get_followers,
         name='get_followers'),
    # GET / PUT / DELETE (only GET is remote)
    path('authors/<int:author_serial>/followers/<path:foreign_author_fqid>',
         follow.handle_follower,
         name='handle_followers'),

    # Follow Request API
    # POST
    # NOTE: Also handles likes
    path('authors/<int:serial>/inbox',
         inbox.recieve_in_inbox,
         name='send_to_inbox'),

    # Posts API
    # GET / DELETE / PUT
    path('authors/<int:author_serial>/posts/<int:post_serial>',
         post.handle_post,
         name='handle_post'),
    
    # GET / POST
    path('authors/<int:pk>/posts',
         post.handle_author_posts,
         name='handle_author_posts'),

    # Image Posts
    path('authors/<int:author_serial>/posts/<int:post_serial>/image',
         image.get_image,
         name='get_image'),
    path('posts/<int:fqid>/image',
         image.get_fqid_image,
         name='get_fqid_image'),

    # Comments API
    # NOTE Inbox handled under Follow Request API
    # GET
    path('authors/<int:author_serial>/posts/<int:post_serial>/comments',
         comment.get_post_comments,
         name="get_post_comments"),
    
    # GET
    path('authors/<int:author_serial>/post/<int:post_serial>/comment/<path:comment_fqid>',
         comment.get_specific_comment,
         name="get_fqid_comment"),
    # GET
    path('comment/<path:fqid>',
         comment.get_fqid_comment,
         name="get_fqid_comment"),

    # Commented API
    # NOTE: Commented includes the non-api URL of the relevant post
    # GET / POST
    path('authors/<int:pk>/commented',
         commented.handle_author_commented,
         name="handle_author_commented"),
    # GET
    path('authors/<path:fqid>/commented',
         commented.get_fqid_author_commented,
         name="get_fqid_author_commented"),
    # GET
    path('authors/<int:author>/commented/<int:comment>',
         commented.get_author_commented,
         name="get_author_commented"),
    # GET
    path('commented/<path:fqid>',
         commented.get_commented,
         name='get_commented'),

    # Likes API
    # NOTE: inbox handled under Follow Request API
    # GET
    path('authors/<int:author_serial>/posts/<int:post_serial>/likes',
         like.get_post_likes,
         name="get_post_likes"),
    # GET
    path('posts/<path:fqid>/likes',
         like.get_fqid_post_likes,
         name="get_fqid_post_likes"),
    # GET
    path('authors/<int:author>/posts/<int:post>/comments/<int:comment>/likes',
         like.get_comment_likes,
         name="get_comment_likes"),
    # GET
    path('liked/<path:like_fqid>',
         like.get_like,
         name="get_like"),       
    # Liked API 
    path('authors/<int:author_serial>/liked',
         liked.get_author_liked,
         name="get_author_liked"),
     path('authors/<int:author_serial>/all_liked', # extra API helper function
         liked.get_author_all_liked,
         name="get_author_all_liked"),
    path('authors/<int:author_serial>/liked/<int:like_serial>',
         liked.get_author_like,
         name="get_author_like"),
    path('authors/<path:author_fqid>/liked/',
         liked.get_fqid_author_liked,
         name="get_fqid_author_liked"),
    # NOTE last one in examples clone from Likes API
    # EXTRA PATHS NOT REQUIRED IN THE SPECS
    path('user/has_liked', 
         other.has_user_liked_post,
         name='has_user_liked_post'),
    path('user/unlike_post', 
         other.user_unlike_post,
         name='user_unlike_post'),
    path('authors/<int:pk>/github_posts',
         other.handle_author_github_posts,
         name='handle_author_github_posts'),
    path('authors/handle_like_post',
         inbox.handle_like_post,
         name="handle_like_post"),
    path('<path:fqid>/create-share',    # Share api
          other.SharePostView.as_view(),
          name='create_share'),
    path('authors/all_likes', # extra API helper function
         like.get_post_all_likes,
         name="get_post_all_likes"),
     
     path('authors/<int:author_serial>/posts/<int:post_serial>/all_comments', # extra API helper function
         comment.get_post_all_comments,
         name="get_post_all_comments"),
     # FQID Paths
         # GET
    path('authors/<path:fqid>',
         author.get_fqid_author,
         name='get_fqid_author'),

     # GET
    path('posts/<path:fqid>/comments',
         comment.get_fqid_post_comments,
         name="get_fqid_post_comments"),

     # GET
    path('posts/<path:fqid>',
         post.get_fqid_post,
         name='get_fqid_post'),
     # Auth stuff
     path('auth/',
          authentication.authenticate,
          name='authenticate'),
     # Auth stuff
     path('auth/test',
          authentication.test_authenticate,
          name='test_authenticate'),
]
