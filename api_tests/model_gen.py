from model_bakery import baker
from honeydew.models import LocalUser, Author, Post, Follow, Like, Comment, Node
from random import choices
from string import ascii_letters, digits
import numpy as np


def rand_str(len=10):
    return "".join(choices(ascii_letters+digits, k=10))

def rand_bytes(len=64):
    return np.random.bytes(len)


def gen_node():
    return baker.make(Node, enable_connection=True)


# Generates a random author
def gen_author(local=True, fqid=None):
    if not local:
        return baker.make(Author, serial=None, local=False)
    return baker.make(Author, serial=None, fqid=fqid, local=True)


# Generates a user
# Can either generate a new author, or not, do what you want
def gen_user(author=None):
    author = gen_author() if author is None else author
    # create_user does hashing so we need to store seperately
    username = rand_str()
    password = rand_str()
    user = LocalUser.objects.create_user(
        username=username,
        password=password,
        author=author,
    )
    user.save()
    return user


# Generates a random post
# If you feel like it, can also generate it's own author
# Public Posts by default
# I don't know how to handle images yet
def gen_post(author=None, visibility=Post.PUBLIC, content_type=Post.TEXT, fqid=None):
    author = gen_author() if author is None else author
    content = rand_bytes() if content_type == Post.IMAGE else rand_str()
    return baker.make(Post,
                      serial=None,
                      fqid=fqid,
                      content=content,
                      content_type=content_type,
                      _fill_optional=['_content_text'],
                      github_activity_id=None,
                      visibility=visibility,
                      author=author)


# Generates a follow
# NOTE God we really should rename that follower/following garbage
# Can generate new authors based on target and follower
def gen_follow(follower=None, target=None):
    follower = gen_author() if follower is None else follower
    target = gen_author() if target is None else target
    return baker.make(Follow, follower=follower, following=target)


# Generate a like
# If no author is given, make a new author to like the post
# If no post is give, make a new post owned by a new author
def gen_like(author=None, post=None):
    author = gen_author() if author is None else author
    post = gen_post() if post is None else post
    return baker.make(Like,
                      serial=None,
                      fqid=None,
                      author=author,
                      post=post)


# Generate a comment
# If no author is given, make a new author that commented on the post
# If no post is given, make a post that is made by a new author.
def gen_comment(author=None, post=None):
    author = gen_author() if author is None else author
    post = gen_post() if post is None else post
    return baker.make(Comment,
                      serial=None,
                      fqid=None,
                      author=author,
                      post=post,
                      content_type=Comment.TEXT)
