from django.db import models
from django.db.models import Max, F, Q
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.core.exceptions import FieldError, ValidationError
from django.utils import timezone
from threading import Lock
from django.core.validators import URLValidator
# NOTE: content_type is limited to:
# text/markdown - common mark
# text/plain # utf-8
# application/base64 # images that are not jpegs or pngs
# image/png;base64
# image/jpeg;base64
#
# I have them all set to charfields, but we can consider models.Choices()
# NOTE: There needs to be some API trickery to handle paging both likes and comments
# NOTE: I have the IDs as models.AutoField for now HOWEVER, we will need to use links for the API
# NOTE: May need to rename fields depending on what other groups use?
HTTP = "https://"
SITE = Site.objects.get_current
author_lock = Lock()
post_lock = Lock()
like_lock = Lock()
likes_lock = Lock()
comment_lock = Lock()
DEFAULT_PFP = "https://i.imgur.com/tEyA1Xc.jpeg"

class Author(models.Model):
    serial = models.IntegerField(blank=True, null=True)  # don't save remote serials
    fqid = models.URLField(unique=True, primary_key=True)
    page = models.URLField()
    host = models.URLField()
    display_name = models.CharField(max_length=4096)
    profile_image = models.URLField(max_length=4096, default=DEFAULT_PFP, blank=True, null=True)
    #profile_image = models.BinaryField(null=True, blank=True, default=None)
    local = models.BooleanField(default=False)
    github = models.URLField(blank=True, null=True, default="")

    """ Handle Creation of our FQID """
    def save(self, *args, **kwargs):  # https://www.geeksforgeeks.org/overriding-the-save-method-django-models/
        # Assume local if no serial or fqid is provided
        if self.local:
            if not self.serial:
                # Should only be scared of race conditions when generating serials
                with author_lock:
                    self.serial = Author.objects.aggregate(Max('serial'))['serial__max']
                    self.serial = (self.serial or 0) + 1
                    self.host = f"{HTTP}{SITE().domain}/api/"
                    self.fqid = f"{self.host}authors/{self.serial}"
                    self.page = f"{HTTP}{SITE().domain}/authors/{self.serial}"
                    super().save(*args, **kwargs)
            else:
                super().save(*args, **kwargs)
        # There should be no case of serial being defined but not fqid
        elif not self.fqid:
            raise FieldError
        else:
            # Save to database
            super().save(*args, **kwargs)
    
    # def clean(self):
    #     super().clean()
    #     if self.github:
    #         validator = URLValidator()
    #         try:
    #             validator(self.github.strip())
    #         except ValidationError:
    #             self.github = None  # Normalize invalid or blank URLs to None
        

class LocalUser(AbstractUser):
    serial = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author,
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL)


class Post(models.Model):
    # Choices for post-type
    PUBLIC = "PUBLIC"
    FRIENDS = "FRIENDS"
    UNLISTED = "UNLISTED"
    DELETED = "DELETED"
    POST_CHOICES = [
        (PUBLIC, 'Public Post'),
        (FRIENDS, 'Friends Only Post'),
        (UNLISTED, 'Unlisted Post'),
        (DELETED, 'Deleted Post'),
    ]

    TEXT = "text/plain"
    MARK = "text/markdown"
    IMAGE = "IMAGE"
    CONTENT_CHOICES = [
        (TEXT, 'Plain Text'),
        (MARK, 'CommonMark'),
        (IMAGE, 'Image Post')
    ]

    serial = models.IntegerField(blank=True, null=True)  # don't save remote serials
    fqid = models.URLField(unique=True, primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=4096)
    content_type = models.CharField(max_length=50, choices=CONTENT_CHOICES, blank=False)  # Probably doesn't need to be too long
    
    #hidden fields
    _content_text = models.TextField(blank=True, null = True)  # Markdown content
    _content_image = models.BinaryField(blank = True, null = True)
    
    published = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=50, choices=POST_CHOICES, blank=False)  # "PUBLIC", "FRIENDS", "UNLISTED", OR "DELETED" TODO: this could be models.Choices
    github_activity_id = models.BigIntegerField(null=True, blank=True) # Unique ID of associated with a GitHub activity.
    shared_post = models.ForeignKey('self', on_delete=models.CASCADE, related_name='shared_posts', null=True, blank=True)
    
    '''
    The following three functions were made with the help of:

    https://dev.to/doridoro/django-model-properties-28ac
    Author: DoriDoro
    Date Accessed: 2024-11-03

    https://django.cowhite.com/blog/dynamic-fields-in-django-rest-framwork-serializers/
    Author: ravi
    Date Accessed: 2024-11-03

    ChatGPT with prompt: "Can this model be changed so that the content field is a BinaryField when the content type is Image and a TextFeild when content_type is TEXT or MARK?"
    '''
    @property
    def content(self):
        if self.content_type in [self.TEXT, self.MARK]:
            return self._content_text
        elif self.content_type == self.IMAGE:
            return self._content_image
        return None

    @content.setter
    def content(self, value):
        if self.content_type in [self.TEXT, self.MARK]:
            self._content_text = str(value)
            self._content_image = None
        elif self.content_type == self.IMAGE:
            if isinstance(value, (bytes, bytearray)):
                self._content_image = value
                self._content_text = None
            else:
                raise TypeError("Content must be bytes for IMAGE content type.")
        else:
            raise ValueError("Invalid content_type specified.")

    def clean(self):
        # Validate that the correct content field is used
        if self.content_type in [self.TEXT, self.MARK] and not self._content_text:
            raise ValidationError("Text content is required for TEXT or MARK content types.")
        if self.content_type == self.IMAGE and not self._content_image:
            raise ValidationError("Image content is required for IMAGE content type.")
         

    """ Handle Creation of our FQID """
    def save(self, *args, **kwargs):  # https://www.geeksforgeeks.org/overriding-the-save-method-django-models/
        # Assume local if no serial or fqid is provided
        if not self.serial and not self.fqid:
            # Should only be scared of race conditions when generating serials
            with post_lock:
                self.serial = Post.objects.filter(author=self.author).aggregate(Max("serial"))['serial__max']
                self.serial = (self.serial or 0) + 1
                self.fqid = f"{self.author.fqid}/posts/{self.serial}"
                self.full_clean() #ensure content type was saved properly
                super().save(*args, **kwargs)
        # There should be no case of serial being defined but not fqid
        elif not self.fqid:
            raise FieldError
        else:
            # Save to database
            self.full_clean() #ensure content type was saved properly
            super().save(*args, **kwargs)

 
class Like(models.Model):
    serial = models.IntegerField(blank=True, null=True)  # don't save remote serials
    fqid = models.URLField(unique=True, primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Actual post object, isntead of URL # Post being liked

    """ Handle Creation of our FQID """
    def save(self, *args, **kwargs):  # https://www.geeksforgeeks.org/overriding-the-save-method-django-models/
        # Set published date if not already set. Fixes a bug where published is set to null.
        if not self.published:
            self.published = timezone.now()

        # Assume local if no serial or fqid is provided
        if not self.serial and not self.fqid:
            # Should only be scared of race conditions when generating serials
            with like_lock:
                self.serial = Like.objects\
                                  .filter(author=self.author)\
                                  .aggregate(Max("serial"))['serial__max']
                self.serial = (self.serial or 0) + 1
                self.fqid = f"{self.author.fqid}/liked/{self.serial}"
            # Save to database
            super().save(*args, **kwargs)
        # There should be no case of serial being defined but not fqid
        elif not self.fqid:
            raise FieldError
        else:
            # Save to database
            super().save(*args, **kwargs)


class Comment(models.Model):

    TEXT = "text/plain"
    MARK = "text/markdown"
    CONTENT_CHOICES = [
        (TEXT, 'Plain Text'),
        (MARK, 'CommonMark'),
    ]

    serial = models.IntegerField(blank=True, null=True)  # don't save remote serials
    fqid = models.URLField(unique=True, primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=50, choices=CONTENT_CHOICES, blank=False)  # Probably doesn't need to be too long
    content = models.TextField()

    """ Handle Creation of our FQID """
    def save(self, *args, **kwargs):  # https://www.geeksforgeeks.org/overriding-the-save-method-django-models/
        # Assume local if no serial or fqid is provided
        if not self.serial and not self.fqid:
            # Should only be scared of race conditions when generating serials
            with comment_lock:
                self.serial = Comment.objects\
                                  .filter(author=self.author)\
                                  .aggregate(Max("serial"))['serial__max']
                self.serial = (self.serial or 0) + 1
                self.fqid = f"{self.author.fqid}/commented/{self.serial}"
                super().save(*args, **kwargs)
        # There should be no case of serial being defined but not fqid
        elif not self.fqid:
            raise FieldError
        else:
            # Save to database
            super().save(*args, **kwargs)


class Follow(models.Model):
    following = models.ForeignKey(Author, related_name="following", on_delete=models.CASCADE)
    follower = models.ForeignKey(Author, related_name="follower", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["follower", "following"],
                                    name="unique_follow_pairs"),
            models.CheckConstraint(check=~Q(following=F('follower')),
                                   name='not_following_self')
        ]

    # This creates a Friendship object between authors if they are following each other.
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if Follow.objects.filter(follower=self.following, following=self.follower).exists():
            Friendship.objects.get_or_create(author1=self.follower,author2=self.following)


# NOTE: Can maybe merge this with a flag for accepted?
class FollowRequest(models.Model):
    summary = models.CharField(max_length=4096)  # NOTE: This just looks kind of optional?
    requestor = models.ForeignKey(Author, related_name="follow_requestor", on_delete=models.CASCADE)
    reciever = models.ForeignKey(Author, related_name="follow_receiver", on_delete=models.CASCADE)


class Friendship(models.Model):
    author1 = models.ForeignKey(Author, related_name='friend1', on_delete=models.CASCADE)
    author2 = models.ForeignKey(Author, related_name='friend2', on_delete=models.CASCADE)


class Node(models.Model):
    # 8.06 I want to be able to add nodes to share with
    host = models.CharField(unique=True, max_length=4096)

    # 8.09 Node to node connections can be authenticated with HTTP Basic Auth
    # Username / Password to Authenticate into THEIR API
    their_username = models.CharField(max_length=4096, null=True, blank=True, default=None)
    their_password = models.CharField(max_length=4096, null=True, blank=True, default=None)

    # Username / Password to Authenticate into OUR API
    our_username = models.CharField(max_length=4096, null=True, blank=True, default=None)
    our_password = models.CharField(max_length=4096, null=True, blank=True, default=None)

    # 8.07 I want to be able to remove nodes and stop sharing with them
    # 8.10 I can disable the node to node interfaces for connections that I no longer want
    enable_connection = models.BooleanField(default=True)


class Colours(models.Model):
    host = models.ForeignKey(Node, on_delete=models.CASCADE)
    color = models.CharField(max_length=4096)
    letter = models.CharField(max_length=4096)
