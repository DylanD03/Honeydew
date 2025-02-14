# Consulted Stackoverflow, Django Documentation, ChatGPT

from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from honeydew.models import Author, Follow, FollowRequest, Post, Friendship, Node, Colours
from api.authentication import encode_basic_auth
from django.db.models import Q
import json
from django.contrib.sites.models import Site
import requests
from django.core.files.storage import FileSystemStorage
import base64
from urllib.parse import urlparse
from api.serializers import AuthorSerializer, FollowRequestSerializer, PostSerializer
from stream.views import friends_list

# View for the author profile page.
def view_author_profile(request, author_id):
    # Check if it is using serial or fqid, then get object accordingly
    if type(author_id) == int:
        author = get_object_or_404(Author, serial=author_id)
    else:
        # NOTE Remote access possible, so we can pull posts
        author = get_object_or_404(Author, fqid=author_id)
        # if remote, pull public/unlisted posts
        if urlparse(author.host).netloc != Site.objects.get_current():
            pull_author_posts(author, request)

    if (request.user.author == author):
        posts = Post.objects.filter(author=author).order_by('-published')
    else:
        posts = Post.objects.filter(author=author, visibility='PUBLIC').order_by('-published')  # Get all public posts by this author and order it by most recent first.

    post_serial = PostSerializer(posts, many=True)
    following_count = len(Follow.objects.filter(follower=author)) # Returns Follow object. Will need to parse Author object in html.
    follower_count = len(Follow.objects.filter(following=author)) # Returns Follow object. Will need to parse Author object in html.
    is_following = Follow.objects.filter(follower=request.user.author, following=author).exists()
    requested = FollowRequest.objects.filter(requestor=request.user.author, reciever=author).exists()
    friend_count = len(Friendship.objects.filter(Q(author1=author) | Q(author2=author)))
    profile_picture = author.profile_image
    
    get_follow_requests = FollowRequest.objects.filter(reciever=author)
    context = {
        'author': author,
        'user': request.user.author,
        'posts': post_serial.data,
        'following_count': following_count,
        'follower_count': follower_count,
        'is_following': is_following,
        'requested': requested,
        'is_own_profile': request.user.author == author,
        'get_follow_request': get_follow_requests,
        'profile_picture': profile_picture,
        'friend_count': friend_count,
    }

    return render(request, 'profile.html', context)

def view_authors(request):
    '''
    This fucntion gets a list of all authors to populate the authors.html template

    @param request: http POST request
    @return: rendered html template
    '''

    #Get all of the authors the logged in author is following
    requester = request.user.author
    following_authors = Follow.objects.filter(follower=requester)
    followed_fqids = following_authors.values_list('following__fqid', flat=True)
    following_authors = Author.objects.filter(fqid__in = followed_fqids)

    # Request Authors from all followed nodes
    get_foreign_authors(request)


    #get all the authors from our database that the current author is not following
    all_athours = Author.objects.all()\
                                .exclude(fqid__in=[requester.fqid] + list(followed_fqids))\
                                .order_by("display_name")
    
    #Get the colors required for the authors badges
    all_athours = get_colors(all_athours)
    following_authors = get_colors(following_authors)

    #render template
    return render(request, 'authors.html', {'user': request.user.author,
                                            'following_authors': following_authors,
                                            'other_authors': all_athours})

def get_foreign_authors(request):
    '''
    This function makes API requests to all of the connected nodes to get their authors.
    The forgein authors are then saved to our database

    @param request: http POST request
    @return: List of all authors
    '''

    for node in Node.objects.filter(enable_connection=True):

        node_host = node.host
        auth_headers = {
            "X-Original-Host": str(request.build_absolute_uri("/api/")),
            'Authorization': encode_basic_auth(node.their_username, node.their_password),
        }
        
        url = f"https://{node.host}/api/authors/"  # HACK size
        
        # Send API request
        try:
            response = requests.get(url, headers=auth_headers)
        except Exception as e:
            print("!!!", e)
            continue
        if response.status_code != 200:
            continue
        
        #Filter authors so we update existing one and add new ones
        authors = response.json().get("authors", [])
        for author in authors:
            ob = Author.objects.filter(fqid=author.get("id"))
            if len(ob) == 0:
                index = author.get("host").find(node_host)
                if index == -1:
                    #only gets authors from this node
                    continue
                else:
                    serializer = AuthorSerializer(data=author, partial=True)
            else:
                ob = ob[0]
                serializer = AuthorSerializer(ob, data=author, partial=True)
            
            #check that the author data is vaild then save new information
            if serializer.is_valid():
                serializer.save(local=False)
               

def get_colors(authors):
    '''
    This function creates a formated data json with the correct author information and their assocaited node color and letter
    
    @param request: a list of author objects
    @return: a formated list of json objects
    '''
    #gets the color and letter for display badge
    all_auth_data = []
    for author in authors:
        host = str(author.host).split("/")[2]
        try:
            if "chartreuse" in host:
                color = "chartreuse"
                letter = "C"
            
            else:
                node = Node.objects.get(host = host)
                colors = Colours.objects.get(host = node)
                color = colors.color
                letter = colors.letter
        except:
            #set defualt colors
            color = "#FF9800"
            letter = "U"

        #format data
        data = {
            "fqid": author.fqid,
            "display_name": author.display_name,
            "color": color,
            "letter": letter,
        }

        #add to master list of authors
        all_auth_data.append(data)

    return all_auth_data

# View who author is following.
def view_author_following(request, author_id):
    # Check if it is using serial or fqid, then get object accordingly
    if type(author_id) == int:
        author = get_object_or_404(Author, serial=author_id)
    else:
        author = get_object_or_404(Author, fqid=author_id)

    following_authors = Follow.objects.filter(follower=author) # Returns Follow object. Will need to parse Author object in html.
    return render(request, 'following.html', {'user': request.user.author,
                                              'following_authors': following_authors})


# View who author's followers are.
def view_author_followers(request, author_id):
   # Check if it is using serial or fqid, then get object accordingly
    if type(author_id) == int:
        author = get_object_or_404(Author, serial=author_id)
    else:
        author = get_object_or_404(Author, fqid=author_id)

    follower_author = Follow.objects.filter(following=author) # Returns Follow object. Will need to parse Author object in html.
    return render(request, 'follower.html', {'user': request.user.author,
                                             'follower_author': follower_author})

# View author's friends.
def view_author_friends(request, author_id):
    #Check if it is using serial or fqid, then get object accordingly
    if type(author_id) == int:
        author = get_object_or_404(Author, serial=author_id)
    else:
        author = get_object_or_404(Author, fqid=author_id)
    friends = friends_list(author.fqid)
    friends_objects = Author.objects.filter(fqid__in = friends)
   
    return render(request, 'friend.html', {'user': request.user.author,
                                           'friend': friends_objects})

# Send author a follow request.
def send_follow_request(request, author_id):
    #Check if it is using serial or fqid, then get object accordingly
    requestor = request.user.author
    if type(author_id) == int:
        author_to_follow = get_object_or_404(Author, serial=author_id)
    else:
        author_to_follow = get_object_or_404(Author, fqid=author_id)
    
    try:
        target_host = urlparse(author_to_follow.host).netloc
        
        # Chartreuse Specific Host Path, they don't follow the host/api/ path. Instead they do host/chartreuse/api/
        if (target_host=="f24-project-chartreuse-b4b2bcc83d87.herokuapp.com"):
            target_host+="/chartreuse"
            

        if target_host != Site.objects.get_current():
            

            # For remote, just assume request accepted (it does not make a different)
            followRequest = FollowRequest.objects.create(
                summary=f"{requestor.display_name} wants to follow {author_to_follow.display_name}!",
                requestor=requestor,
                reciever=author_to_follow)
            
            serializer = FollowRequestSerializer(followRequest)
            node = Node.objects.get(host=target_host, enable_connection=True)
         
            auth_headers = {
                "X-Original-Host": str(request.build_absolute_uri("/api/")),
                'Authorization': encode_basic_auth(node.their_username, node.their_password),
            }
          
            response = requests.post(f"{author_to_follow.fqid}/inbox",
                                     json=serializer.data,
                                     headers=auth_headers)
            if response.status_code not in [200, 201]:
                uploaded = serializer.data
                error = response.json()
            
                raise Exception

            # In remote, we can assume that remote authors just accept
            follow = Follow.objects.create(follower=requestor, following=author_to_follow)
            follow.save()
        else:
            # We can store requests properly in local
            reciever = author_to_follow
            followRequest = FollowRequest.objects.create(requestor=requestor, reciever=reciever)
            followRequest.save()
        return redirect('view_author_profile', author_id)

    except Exception as e:
        return redirect('view_author_profile', author_id)


# Unfollow an author.
def unfollow_author(request, author_id):
    #Check if it is using serial or fqid, then get object accordingly
    if type(author_id) == int:
        author_to_unfollow= get_object_or_404(Author, serial=author_id)
    else:
        author_to_unfollow = get_object_or_404(Author, fqid=author_id)

    follower = request.user.author

    try:
        follow_instance = Follow.objects.get(follower=follower, following=author_to_unfollow)
        follow_instance.delete()
        # check if authors are friends.
        author_friendships = Friendship.objects.filter(Q(author1=request.user.author) | Q(author2=request.user.author))

        friendship = author_friendships.filter(Q(author1=author_to_unfollow) | Q(author2=author_to_unfollow))
        # If a friendship exists, delete the friendship when unfollowed.
        if friendship:
            friendship.delete()

    except Follow.DoesNotExist:
        pass

    return redirect('view_author_profile', author_id=author_id)


# Edit author profile page.
def edit_profile(request, author_id):
    # Check if it is using serial or fqid, then get object accordingly
    if type(author_id) == int:
        author = get_object_or_404(Author, serial=author_id)
    else:
        author = get_object_or_404(Author, fqid=author_id)

    if (request.user.author != author):
        return redirect('stream-home')

    if request.method == 'POST':
        author.display_name = request.POST.get('display_name', author.display_name)
        author.github = request.POST.get('github-url', author.github)
        author.profile_image = request.POST.get('profile_picture', '')
        author.save()
        return redirect('view_author_profile', author_id=author.serial)
    return render(request, 'edit_profile.html', {'user': request.user.author,
                                                 'author': author})


# View author's follow requests.
def view_follow_requests(request, author_id):
    # If the author is remote, panic
    if type(author_id) != int:
        return HttpResponse(status=500)

    author = get_object_or_404(Author, serial=author_id)
    follow_requests = FollowRequest.objects.filter(reciever=author)
    follow_request_serial = FollowRequestSerializer(follow_requests, many = True)
    author_serial = AuthorSerializer(author)
    context = {
        "follow_requests": follow_request_serial.data,
        'user': request.user.author,
        "author": author_serial.data
    }
    
    i = 0
    for follows in follow_request_serial.data:
        i += 1
    return render(request, "follow_requests.html", context)


# Accept a follow request.
def accept_follow_request(request, author_id, requester_id):

    requester = Author.objects.get(fqid=requester_id)
    reciever = Author.objects.get(fqid=author_id)
    follow_request = FollowRequest.objects.filter(requestor=requester,
                                                  reciever=reciever)
    if len(follow_request):
        try:
            Follow.objects.create(follower=requester, following=reciever)
        except Exception:
            pass
        follow_request[0].delete()
    return redirect('view_follow_requests', author_id=reciever.serial)


# Deny a follow request.
def deny_follow_request(request, author_id, requester_id):

    follow_request = FollowRequest.objects.filter(requestor__fqid=requester_id,
                                                  reciever__fqid=author_id)
    if len(follow_request) > 0:
        follow_request.delete()
    return redirect('view_follow_requests', author_id=request.user.author.serial)


def pull_author_posts(author, request):
    
    url = f"{author.fqid}/posts?size=200"  # unpaged
    host = urlparse(url).netloc
    
    # Chartreuse Specific Host Path, they don't follow the host/api/ path. Instead they do host/chartreuse/api/
    if (host=="f24-project-chartreuse-b4b2bcc83d87.herokuapp.com"):
        host+="/chartreuse"
       
    # Figure out if node is one of our connections
    # NOTE remote node should take responsibility to reject requests
    node = Node.objects.filter(host=host, enable_connection=True)
    if not node:
        return
    node = node[0]
    auth_headers = {
        "X-Original-Host": str(request.build_absolute_uri("/api/")),
        'Authorization': encode_basic_auth(node.their_username, node.their_password),
    }
    
    # Otherwise, make request
    try:
        response = requests.get(url, headers=auth_headers)
    except Exception:
        pass
  
    posts = response.json().get("src", [])

    # Then, serialize and store posts that we retrieve
    for post in posts:
        ob = Post.objects.filter(fqid=post.get("id"))
        content = post.get("content", "")
        if post["contentType"] == "IMAGE":
            try:
                # Decode the base64 content into bytes
                
                content_bytes = base64.b64decode(post["content"].strip())
            except Exception as e:
                continue
        else:
            content_bytes = content
    
        if len(ob) == 0:
            author_data = post.pop('author')
            author = Author.objects.get(fqid=author_data['id'])
            post = Post.objects.create(
                author=author,
                title=post["title"] or "",
                fqid=post["id"],
                description=post["description"] or "",
                content_type=post["contentType"] or "",
                content=b"e",
                visibility=post["visibility"])
            post.content = content_bytes
            post.save()