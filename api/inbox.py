from urllib.parse import urlparse
import json
from django.shortcuts import redirect, get_object_or_404
import requests
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .authentication import encode_basic_auth, CustomAuthentication
from .serializers import AuthorSerializer, FollowRequestSerializer, CommentSerializer, LikeSerializer
import base64
from honeydew.models import Author, Post, Follow, Node, Like, Comment
from stream.views import friends_list
from django.contrib.sites.models import Site


@api_view(['POST'])
@authentication_classes([CustomAuthentication])  # Apply custom authentication to this API function
@permission_classes([IsAuthenticated])
def recieve_in_inbox(request, serial):
    print("****************IN INBOX*********************")
    print("Request Header:", request.headers)
    print("Request Data:", request.data)

    try:
        # POST [remote]: send a like object to AUTHOR_SERIAL
        if request.data.get("type") == "like":
            print("INBOX LIKE OBJECT RECEIVED")

            # Ensure Like's Author is in the Database
            author_data = request.data.get("author")
            print("Author: ", author_data)
            if not Author.objects.filter(fqid=author_data.get('id')).exists():
                author_serializer = AuthorSerializer(data=author_data)
                if author_serializer.is_valid():
                    author_serializer.save()
                    print("INBOX LIKE saving author: ", author_serializer.data)
                else:
                    print("INBOX LIKE AUTHOR NOT FOUND: ")
                    return Response(status=400, data=author_serializer.errors)

            # Retrieve the actual Author instance after saving
            author_instance = Author.objects.get(fqid=author_data.get('id'))
            print("Actual isntance: ", author_instance)

            # Use the Author instance in the Like data
            like_data = request.data.copy()  # Make a mutable copy of the request data
            like_data['author'] = author_instance  # Assign the Author instance to the Like
            print("LIKE DATA: ", like_data)

            # Ensure Post instance Exists
            print("CHECK POST INSTNACE EXISTS")
            if not Post.objects.filter(fqid = request.data.get("object")).exists():
                print("INBOX LIKE POST NOT FOUND: ")
                # TODO: Perhaps GET post from fqid.
                return Response(status=400, data={"error": "Post object not found for the given ID."})
            print("RETRIEVE POST INSTANCE")
            # Retrieve Post instance
            post_instance = Post.objects.get(fqid = request.data.get("object"))
            print("POST INSTANCE RETRIEVED: ", post_instance)

            # Save the Like itself into the Database
            print("SAVE LIKE INTO DB")
            like = Like.objects.filter(fqid = request.data.get("id"))
            print("CHECK IF LIKE EXISTS??", like)
            if not like.exists(): # Sanity check. Ensure like is only added once
                print("LIKE DOES NOT EXIST, WE MAKE NEW ONE")
                try:
                    like_instance = Like.objects.create(
                        fqid=request.data.get("id"),
                        author=author_instance,  # Assign the actual Author instance
                        post = post_instance,
                        published=request.data.get("published"),
                    )
                    print("NEW LIKE INSTNACE", like_instance)
                    like_instance.save()
                except Exception as e:
                    print("INBOX SAVING LIKE INSTANCE BROKE", str(e))
                    return Response(status=400, data={"error": str(e)})

            print("SUCCESS??", "200")
            return Response(status=200)

        elif request.data.get("type") == "follow":
            print("###################IN FOLLOW###########################")
            print(" In follow part of the inbox ")

            # HACK Handle potentially incomplete target author
            data = request.data
            obj_fqid = data["object"]["id"]
            if data["object"]["github"] == "" or data["object"]["github"] == "None":
                data["object"].pop('github')
            obj = get_object_or_404(Author, fqid=obj_fqid, local=True)
            data["object"] = AuthorSerializer(obj).data
            print('pass get author') 

            print("actor git: ", data["actor"]["github"])
            if data["actor"]["github"] == "" or data["actor"]["github"] == "None":
                print("popped github")
                data["actor"].pop('github')

            # Finalize Request
            request_serializer = FollowRequestSerializer(data=data)
            print("serial", request_serializer)

            if not request_serializer.is_valid():
                print("------Serial not Vaild------")
                print(request_serializer.errors)
                print(request_serializer.data)
                print(data)
                return Response(status=400, data=request_serializer.errors)

            request_serializer.save()
            return Response(status=201, data=request_serializer.data)

        elif request.data.get("type") == "comment":
            print("+++++++Comment to inbox++++++++")
            # Ensure Post's Author is in the Database
            author_data = request.data.get("author")
            print("After author data")
            if not Author.objects.filter(fqid=author_data.get('id')).exists():
                print("In if not author data")
                author_serializer = AuthorSerializer(data=author_data)
                print("After author serial")
                if author_serializer.is_valid():
                    print("After vaild")
                    author_serializer.save()
                else:
                    print("*************In Author Exception***********")
                    return Response(status=400, data=author_serializer.errors)

            # Retrieve the actual Author instance after saving
            author_instance = Author.objects.get(fqid=author_data.get('id'))
            print("After author instance")

            #Ensure Post is in Database
            print("Post fqid?", type(request.data.get("post")))
            if not Post.objects.filter(fqid=request.data.get("post")).exists():
                print("in no post section")
                return Response(status=400, data="No such post.")

            # Retrieve the actual Author instance after saving
            post_instance = Post.objects.get(fqid=request.data.get("post"))
            print("After post instance", type(post_instance))

            # Save the Post itself into the Database
            comment = Comment.objects.filter(fqid = request.data.get("id"))
            print("After get comment")
            if not comment.exists(): # Sanity check. Ensure post is only added once

                print("In not exists")
                try:
                    print(f"fqid= {request.data.get('id')} \npost = {post_instance}\ncontent_type= {request.data.get('contentType')}\ncontent= {request.data.get('comment')}\nauthor= {author_instance}\npublished= {request.data.get('published')}")
                    post_instance = Comment.objects.create(
                    fqid= request.data.get("id"),
                    post = post_instance,
                    content_type=request.data.get("contentType"),
                    content=request.data.get("comment"),
                    author=author_instance,  # Assign the actual Author instance
                        published=request.data.get("published"),
                    )
                    post_instance.save()
                except Exception as e:
                    print("*************In Comment Exception***********")
                    print("error:", e)
                    return Response(status=400, data={"error": str(e)})

                return Response(status=201)

            else:
                return Response(status=400, data="Comment Exists")

        elif request.data.get("type") == "post":
            print("In Post Part of Inbox")

            # Ensure Post's Author is in the Database
            author_data = request.data.get("author")
            print("After author data")
            if not Author.objects.filter(fqid=author_data.get('id')).exists():
                print("In if not author data")
                author_serializer = AuthorSerializer(data=author_data)
                print("After author serial")
                if author_serializer.is_valid():
                    print("After vaild")
                    author_serializer.save()
                else:
                    print("*************In Author Exception***********")
                    return Response(status=400, data=author_serializer.errors)

            # Retrieve the actual Author instance after saving
            author_instance = Author.objects.get(fqid=author_data.get('id'))
            print("After author instance")
            # Use the Author instance in the post data
            post_data = request.data.copy()  # Make a mutable copy of the request data
            print("After post data")
            post_data['author'] = author_instance  # Assign the Author instance to the post
            print("After set author data")

            # HACK just assume base64 stuff has images
            content_type = post_data.get("contentType")
            # Get content type for image (assume only images are base64)
            is_image = True if "base64" in content_type\
                else False
            # Our Post.IMAGE type is kind of trash but we roll with it
            content_type = Post.IMAGE if is_image\
                else content_type

            # Parse the content string
            content = post_data.get("content")
            if is_image:
                # Cut out possible beginning tags.
                # Just trust the process that it's base64,
                loc = content.find("base64,")
                content = content[loc+len("base64,"):]
                content = base64.b64decode(content)

            print(content)
            # Save the Post itself into the Database
            post = Post.objects.filter(fqid=request.data.get("id"))
            print("After get post")
            if not post.exists():  # Sanity check. Ensure post is only added once
                print("In not exists")
                try:
                    post_instance = Post.objects.create(
                        fqid=post_data.get("id"),
                        title=post_data.get("title") or " ",
                        description=post_data.get("description") or " ",
                        content_type=content_type,
                        content=content or " ",
                        author=author_instance,  # Assign the actual Author instance
                        published=post_data.get("published"),
                        visibility=post_data.get("visibility"),
                    )
                    post_instance.save()
                except Exception as e:
                    print("*************In Post Exception***********")
                    local = locals()
                    print("\n".join([f"{k}: {local[k]}" for k in locals()]))
                    print("error:", e)
                    return Response(status=400, data={"error": str(e)})
            else:
                # update the post
                print("in else")
                post = post[0]
                post.title = post_data.get("title") or " "
                post.description = post_data.get("description") or " "
                post.content = content or " "
                post.visibility = post_data.get("visibility")

                post.content_type = content_type
                post.published = post_data.get("published")
                post.save()

            return Response(status=200)

        else:
            print(" Did not find a type match ")
            return Response(status=304)
    except Exception as e:
        print("ERROR", str(e))
        local = locals()
        local = "\n".join([f"{k}: {local[k]}" for k in local])
        print(local)
        return Response(status=500, data={"error": str(e)})


# Here as an easy way for me to understand where push requests are sent
def push_to_followers(serializer, author):
    print("++++++++++++++++++++PUSH TO FOLLOWERS++++++++++++++++++")
    print(serializer.data)
    # ASSUMES THAT THESE ARE VALID
    # WILL IGNORE ERRORS IN CONNECTION
    follows = Follow.objects.filter(following=author)
    nodes = Node.objects.filter(enable_connection=True)
    hostnames = {n.host for n in nodes}

    # NOTE Probably wastes a lot of requests?
    # If we don't have notifications, we only need one-per-node
    for follow in follows:
        url = f"{follow.follower.fqid}/inbox"
        host = urlparse(url).netloc

        # Chartreuse Specific Host Path, they don't follow the host/api/ path. Instead they do host/chartreuse/api/
        if (host=="f24-project-chartreuse-b4b2bcc83d87.herokuapp.com"):
            host+="/chartreuse"
            print("chartreuse host: ", host)

        # Follower is connect to an enabled node
        if host not in hostnames:
            continue
        node = nodes.get(host=host)
        auth_headers = {
            'X-Original-Host': f"https://{Site.objects.get_current()}/api/",
            'Authorization': encode_basic_auth(node.their_username, node.their_password),
            'Content-Type': 'application/json',
        }
        try:
            response = requests.post(url, json=serializer.data, headers=auth_headers)
        except Exception as e:
            print(e)


def push_to_friends(serializer, author):
    # Get friends
    friend_fqids = friends_list(author.fqid)

    nodes = Node.objects.filter(enable_connection=True)
    hostnames = {n.host for n in nodes}

    for fqid in friend_fqids:
        url = f"{fqid}/inbox"
        host = urlparse(url).netloc

        # Chartreuse Specific Host Path, they don't follow the host/api/ path. Instead they do host/chartreuse/api/
        if (host=="f24-project-chartreuse-b4b2bcc83d87.herokuapp.com"):
            host = host + "/chartreuse"
            print("chartreuse host: ", host)

        # Follower is connect to an enabled node
        if host not in hostnames:
            continue
        node = nodes.get(host=host)
        auth_headers = {
            'X-Original-Host': f"https://{Site.objects.get_current()}/api/",
            'Authorization': encode_basic_auth(node.their_username, node.their_password),
            'Content-Type': 'application/json',
        }
        try:
            response = requests.post(url, json=serializer.data, headers=auth_headers)
        except Exception:
            pass  # Just don't self destruct if pushing fails


def push_to_owner(serializer, author):
    # Push serialized object to author
    url = f"{author.fqid}/inbox"
    host = urlparse(url).netloc

    # Chartreuse Specific Host Path, they don't follow the host/api/ path. Instead they do host/chartreuse/api/
    if (host=="f24-project-chartreuse-b4b2bcc83d87.herokuapp.com"):
        host = host + "/chartreuse"
        print("chartreuse host: ", host)
    
    node = Node.objects.filter(host=host, enable_connection=True)

    # If length is 0, we don't have a connection and don't push
    if len(node) == 0:
        return
    node = node[0]

    auth_headers = {
        'X-Original-Host': "fhttps://{Site.objects.get_current()}/api/",
        'Authorization': encode_basic_auth(node.their_username, node.their_password),
        'Content-Type': 'application/json',
    }
    try:
        response = requests.post(url, json=serializer.data, headers=auth_headers)
    except Exception:
        pass  # Just don't self destruct if pushing fails


@api_view(['POST'])
def handle_like_post(request):
    """
    Create a Like Object, to indicate that a User has liked the author's post.

    Parameters:
    - (URL)  user_serial: The serial number of the user
    - (body) post_serial: The serial number of the post
    - (body) author_serial: The serial number of the author who made the post

    Returns:
    - String indicating success or error
    """
    print("***** in handle_like_post *****")
    body_data = json.loads(request.body)
    # Get Post objects from database
    post_fqid = body_data.get('post_fqid')
    author_fqid = body_data.get('author_fqid')
    user_fqid = body_data.get('user_fqid')  # User that clicked the 'like' button
    print("POST_fqid: ", post_fqid, "USER_fqid: ", user_fqid)
    post = get_object_or_404(Post, author__fqid=author_fqid, fqid=post_fqid)
    print(post)

    # Get author that liked the post
    user = get_object_or_404(Author, fqid=user_fqid)
    print("AUTHOR THAT LIKED POST: ", user)

    # Create and Save a Like Object
    like = Like(author=user, post=post)
    like.save()
    like_serializer = LikeSerializer(like)
    print("LIKE SERIALIZER.DATA: ", like_serializer.data)


    # Push serialized object to author
    print("about to push")
    url = f"{post.author.fqid}/inbox"
    host = urlparse(url).netloc

    # Chartreuse Specific Host Path, they don't follow the host/api/ path. Instead they do host/chartreuse/api/
    if (host=="f24-project-chartreuse-b4b2bcc83d87.herokuapp.com"):
        #f24-project-chartreuse-b4b2bcc83d87.herokuapp.com
        host = host + "/chartreuse"
        
    node = Node.objects.filter(host=host, enable_connection=True)
    print("URL: ", url, "HOST: ", host, "NODE: ", node)

    # If length is 0, we don't have a connection and don't push
    if len(node) == 0:
        print("LENGTH NODE = 0: ", node)
        return Response(like_serializer.data)
    node = node[0]

    auth_headers = {
        'X-Original-Host': f"https://{Site.objects.get_current()}/api/",
        'Authorization': encode_basic_auth(node.their_username, node.their_password),
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(url, json=like_serializer.data, headers=auth_headers)
    except Exception:
        local = locals()
        print("\n".join([f"{k}: {local[k]}" for k in local]))
        print("Exeption Occured while propogating likes to other Nodes ")
        pass  # Just don't self destruct if pushing fails

    # Return like object
    return Response(like_serializer.data)
