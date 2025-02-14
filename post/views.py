from datetime import datetime

from django.shortcuts import redirect, render, get_object_or_404

from api.inbox import push_to_followers, push_to_friends, push_to_owner
from api.serializers import PostSerializer, CommentSerializer
from honeydew.models import Post, Comment


# Create your views here.
def index(request):
    '''
    This function redirects users to a UI to select the type of post they want to make
    @param request: http POST request
    @return: redirect to content_type selection page
    '''

    content_types = Post.CONTENT_CHOICES
    return render(request, "post/post_type.html", {'content_types': content_types})

def get_type(request):
    '''
    This function redirects users to a UI to create a post
    @param request: http POST request
    @return: redirect to page to create post
    '''
    type = request.POST.get('content_type')
    post_types = Post.POST_CHOICES[:-1]  # NOTE Assumes that DELETED is last

    return render(request, "post/post_make.html", {'post_types': post_types,
                                                   'content_type': type})


def create_post(request):
    '''
    This function creates a new post object
    @param request: http POST request
    @return: redirect to stream
    '''
    print(request.POST)
    print(request.FILES)
    if request.method == 'POST':

        #handle images vs text
        content_type = request.POST.get('content_type')
        if content_type == "IMAGE":
            post_image = request.FILES.get('post_image')
            print(type(post_image))
            content = post_image.read()
        else:
            content = request.POST.get('content')


        post = Post.objects.create(
            author=request.user.author,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            content_type=content_type,
            content=content,
            visibility=request.POST.get('visibility')
        )
        post.save()

        # Send this new post to all Nodes connected to this Node.
        serializer = PostSerializer(post)
        if post.visibility == Post.FRIENDS:
            push_to_friends(serializer, request.user.author)
        else:
            push_to_followers(serializer, request.user.author)
    return redirect('stream-home')

def edit_post(request, fqid):
    '''
    This function redirects users to an edit post view
    @param request: http POST request
    @param fqid: the fqid (unique URL) of the post to be edited
    @return: redirect to post_edit page or stream
    '''
    if request.method == 'POST':
        post = get_object_or_404(Post, fqid=fqid)
        post = PostSerializer(post)
        post_types = Post.POST_CHOICES
        return render(request, 'post/post_edit.html' , {'post': post.data, 'post_types': post_types})
    else:
        return redirect('stream-home')

def delete_post(request, fqid):
    '''
    This function deleted a post
    @param request: http POST request
    @param fqid: the fqid (unique URL) of the post to be deleted
    @return: redirect to stream
    '''

    #TODO: Update to a Put function instead of POST (for images)
    post = get_object_or_404(Post, fqid=fqid)
    if request.method == "POST":
        original_visibility = Post.visibility
        post.visibility = Post.DELETED
        post.save()

        serializer = PostSerializer(post)
        push_to_friends(serializer, post.author) \
            if original_visibility == Post.FRIENDS\
            else push_to_followers(serializer, post.author)

        return redirect('stream-home')  # Redirect to stream home

def save_edit(request, fqid):
    '''
    This saves the edits made to a post
    @param request: http POST request
    @param fqid: the fqid (unique URL) of the post to be saved after an edit
    @return: redirect to stream to see updated post
    '''

    #handle images vs text
    content_type = request.POST.get('content_type')
    if content_type == "IMAGE":
        post_image = request.FILES.get('post_image')
        print(type(post_image))
        content = post_image.read()
    else:
        content = request.POST.get('content')

    post = get_object_or_404(Post, fqid=fqid)
    post.title=request.POST.get('title')
    post.description=request.POST.get('description')
    post.content=content
    post.visibility=request.POST.get('visibility')
    post.published = datetime.now()
    post.save()

    serializer = PostSerializer(post)

    push_to_friends(serializer, post.author) \
        if post.visibility == Post.FRIENDS\
        else push_to_followers(serializer, post.author)

    return redirect('stream-home')

def create_comment(request, fqid):
    '''
    This function creates a new comment object
    @param request: http POST request
    @param fqid: the fqid (unique URL) of the post that the comment was made on
    @return: redirect to the post's page
    '''
    post = get_object_or_404(Post, fqid=fqid)
    if request.method == 'POST':
        comment = Comment.objects.create(
            author=request.user.author,
            post=post,
            content_type=request.POST.get('content_type'),
            content=request.POST.get('content'),
        )
        comment.save()

    serializer = CommentSerializer(comment)
    push_to_owner(serializer, post.author)
    push_to_friends(serializer, post.author)\
        if post.visibility == Post.FRIENDS\
        else push_to_followers(serializer, post.author)

    return redirect('view_post', post.fqid)
