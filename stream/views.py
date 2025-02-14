from django.shortcuts import render, redirect, get_object_or_404
from honeydew.models import Post, Like, Comment, Follow, Friendship
from api.serializers import PostSerializer, CommentSerializer, PostsSerializer
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import base64
import re
import copy



#  Create your views here.
def stream_home(request):
    '''
    This fucntion collects all the posts and renders the stream page
    @param request: http POST request
    @return: rendered html template

    '''
    #  Redirect to Login Page if user is signed out
    if not request.user.is_authenticated or request.user.author is None:
        return redirect('login')  #  Redirect to the login page

    # get all public posts
    public_posts = Post.objects.filter(visibility = 'PUBLIC').exclude(visibility = 'DELETED')

    # get unlisted posts of those I am following
    fqid = request.user.author.fqid
    followed_authors = list(Follow.objects.filter(follower = fqid).values_list('following', flat = True))
    follows_posts = Post.objects.filter(author__in = followed_authors, visibility = 'UNLISTED')
    
    #get friends only posts
    friends_post = get_friendsonly(fqid)
    
    # get currnet users posts
    my_posts = Post.objects.filter(author = fqid).exclude(visibility = 'DELETED')


    # join all posts
    posts = public_posts.union(follows_posts)
    posts = posts.union(my_posts)
    posts = posts.union(friends_post).order_by('-published')

    #paginate posts
    serializer, paginated_posts = paginator(posts, request)

    content_types = Comment.CONTENT_CHOICES

    for post in serializer.data:
        if 'author' in post:
            # Set default for 'github' to empty string
            author = post['author']
            author['github'] = author.get('github') or ""
    
    return render(request, 'stream/stream.html', {'user': request.user.author, 'posts':serializer.data, "content_types":content_types, "page_obj":paginated_posts  })


def get_friendsonly(fqid):
    '''
    This fuction gets friends only posts

    @param fqid: fqid of author
    @return: list of friends only post
    '''
    # get friends only posts of my friends
    friend1 = Friendship.objects.filter(author1 = fqid).values_list('author2', flat = True)
    friend2 = Friendship.objects.filter(author2 = fqid).values_list('author1', flat = True)
    friends = list(friend1.union(friend2))
    # print(friends)
    friends_post = Post.objects.filter(author__in = friends, visibility = 'FRIENDS')

    return friends_post



def paginator(posts, request):
    '''
    This fuction paginates the posts to display on the stream

    @param request: http POST request
    @param posts: a list of posts
    @return: posts serializer
    '''

    # Paginate the posts # Credit: https://stackoverflow.com/a/74619754
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page = request.GET.get('page') # 'page' parameter is sent by stream.html when you click on the next/previous buttons.
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)
    serializer = PostSerializer(paginated_posts, many=True)

    return serializer, paginated_posts

def view_post(request, id):
    '''
    This fucntion gets the information for a post then renders a post view page

    @param request: http POST request
    @param id: posts id
    @return: rendered html template

    '''
    print("post_id:", id)

    # get object and serilize
    post = get_object_or_404(Post, pk=id)
    serializer = PostSerializer(post)

    #get the current users fqid
    user_fqid = request.user.author.fqid

    #check if the current user has permissions to view the post
    perms, is_mine = check_perms(post, user_fqid)
    if not perms:
        messages.info(request, 'You do not have permission to view this post')
        return redirect('stream-home')


    serial = re.sub(r"\D", "", serializer.data["id"])

    # get like and comment count
    like_count = Like.objects.filter(post = id).count()
    comments = Comment.objects.filter(post = id).order_by('-published')
    comment_count = comments.count()
    comment_serializer = CommentSerializer(comments, many = True)

    # get content type for comments
    content_types = Comment.CONTENT_CHOICES

    post_data = copy.deepcopy(serializer.data)

    # Set default for 'github' to empty string
    print("Author Github: ", post_data['author'].get('github'))
    if (post_data['author'].get('github') == None) or (post_data['author'].get('github') == "None"):
        print("None")
        post_data['author']['github'] =  " "
    print("Author Github AFter: ", post_data['author'].get('github'))


    return render(request, "stream/post_view.html", {"post": post_data, "likes": like_count, "comment_count": comment_count, "comments": comment_serializer.data, "mine": is_mine, "serial": serial, 'content_types': content_types, 'user': request.user.author})

def check_perms(post, user_serial):
    '''
    This fucntion checks if a user has permission to view a post
    @param post: post object
    @param user_serial: serial of the user who wants to view the post
    @return: bool for permission status
    '''

    #check if the user owns the post
    author_serial = post.author.fqid
    is_mine = False
    if user_serial == author_serial:
        is_mine = True

    # get list of friends
    friends = friends_list(user_serial)
    print("friends: ", friends)
    print("Visablity: ", post.visibility)

    # don't allow non-friends of poster to view the post
    if post.visibility == "FRIENDS":
        print("in-friends only")
        if is_mine == False and author_serial not in friends:
            return False

    # not allowed to view deleted posts
    if post.visibility == 'DELETED':
        return False
        
    return True, is_mine

def friends_list(fqid):
    '''
    This function gets a list of all of an authors friends

    @param fqid: author FQID
    @return: list of friends objects
    '''
    friend1 = Friendship.objects.filter(author1=fqid)\
                                 .values_list('author2', flat=True)
    friend2 = Friendship.objects.filter(author2=fqid)\
                                .values_list('author1', flat=True)
    friends = list(friend1.union(friend2))

    return friends
