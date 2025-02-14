from rest_framework import serializers
from honeydew.models import Like, Author, Comment, Post, FollowRequest
import base64
import imghdr
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
# from .models import


DEFAULT_PFP = "https://imgur.com/gallery/mare-foal-fhv3QDB#/t/art"


class AuthorSerializer(serializers.Serializer):
    type = serializers.CharField(default="author", read_only=True)
    id = serializers.URLField(source="fqid")
    host = serializers.URLField()
    displayName = serializers.CharField(source="display_name")
    github = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    profileImage = serializers.URLField(source="profile_image", default=DEFAULT_PFP, allow_blank=True, allow_null=True)
    #profileImage = serializers.ImageField(source="profile_image")
    page = serializers.URLField()

    class Meta:
        model = Author
        fields = ("type", "id", "host", "displayName", "profileImage", "page")

    def to_internal_value(self, data):
        '''
        This function was made with the help of:

        ChatGPT with prompt: How can you update a serializer to deal with a URL field sent as an empty string or as 'None'?
        '''
        if "github" in data and data['github'] in ["", "None"]:
            data["github"] = None
        return super().to_internal_value(data)

    def validate_profileImage(self, value):
        if value == "" or value is None:
            return DEFAULT_PFP
        return value

    def get_profileImage(self, value):
        return DEFAULT_PFP if value is None else value

    def update(self, instance, validated_data):
        # Update existed Author object with validated data
        # Only these should matter I think?
        instance.display_name = validated_data.get("display_name",
                                                   instance.display_name)
        print("before instance in github")
        instance.github = validated_data.get("github",
                                             instance.github)
        instance.save()
        return instance

    def create(self, validated_data):
        return Author.objects.create(**validated_data)


class AuthorsSerializer(serializers.Serializer):
    type = serializers.CharField(default="authors", read_only=True)
    authors = AuthorSerializer(many=True, read_only=True)


class FollowRequestSerializer(serializers.Serializer):
    type = serializers.CharField(default="follow", read_only=True)
    summary = serializers.CharField()
    actor = AuthorSerializer(source="requestor")
    object = AuthorSerializer(source="reciever")

    def validate_actor(self, value):
        """
        Checks if:
            - The actor is already on our database or...
            - the information provided by "actor" is enough to create
              Author Data
                - TODO Maybe update too?
        """
        # If lookup succeeds, we are done, and the actor exists
        # Author data might be inconsistent, but oh wel
        # print("Received actor data:", value)  # Debugging output

        # # Validate the 'github' field
        # if "github" in value:
        #     github = value["github"]
        #     if github:
        #         github = github.strip()  # Remove leading/trailing whitespace
        #         validator = URLValidator()
        #         try:
        #             validator(github)  # Validate the URL
        #         except ValidationError:
        #             github = None  # Invalid URL; set to None
        #     value["github"] = github  # Update the value

        # Check if the author exists
        if Author.objects.filter(fqid=value["fqid"]).exists():
            return value

        # Otherwise, create the Author instance
        try:
            obj = Author.objects.create(**value)
            print("Created new Author:", obj)
        except Exception as e:
            print("Failed to create Author:", e)
            raise e
        return value

    def create(self, validated_data):
        # source field automatically does renaming c:
        requestor_data = validated_data.pop("requestor")
        reciever_data = validated_data.pop("reciever")

        requestor = Author.objects.get(fqid=requestor_data["fqid"])
        reciever = Author.objects.get(fqid=reciever_data["fqid"])
        requestor.save()
        reciever.save()
        return FollowRequest.objects.create(requestor=requestor,
                                            reciever=reciever,
                                            **validated_data)


class FollowersSerializer(serializers.Serializer):
    type = serializers.CharField(default="Followers")
    followers = AuthorSerializer(many=True, read_only=True)


class CommentSerializer(serializers.Serializer):
    type = serializers.CharField(default="comment", read_only=True)
    id = serializers.URLField(source="fqid")
    author = AuthorSerializer()
    comment = serializers.CharField(source="content")
    contentType = serializers.CharField(source="content_type")
    published = serializers.DateTimeField()
    post = serializers.URLField(source='post.fqid')
    #likes = serializers.JSONField()

    def create(self, validated_data):
        # Create comment instance with validated_data
        # But I need something for model creation
        return Comment.objects.create(**validated_data)

    # I don't think there's any need to edit comments??


class CommentsSerializer(serializers.Serializer):
    # NOTE only for organizing comments on posts
    type = serializers.CharField(default="comments", read_only=True)
    id = serializers.URLField()
    page = serializers.URLField()
    page_number = serializers.IntegerField(default=1)
    size = serializers.IntegerField(default=5)
    count = serializers.IntegerField()
    src = CommentSerializer(many=True, read_only=True)


class LikeSerializer(serializers.Serializer):

    type = serializers.CharField(default="like", read_only=True)
    id = serializers.URLField(source="fqid")
    author = AuthorSerializer()  # Nested Serializer to parse Author
    object = serializers.URLField(source='post.fqid')  # get fqid of post
    published = serializers.DateTimeField()

    def create(self, validated_data):
        # Create like instance with validated_data
        return Like.objects.create(**validated_data)


class PostSerializer(serializers.Serializer):
    type = serializers.CharField(default="post", read_only=True)
    id = serializers.URLField(source="fqid")
    title = serializers.CharField()
    description = serializers.CharField()
    contentType = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    author = AuthorSerializer()
    # comments = serializers.ListField(default=[], read_only=True)
    # likes = serializers.ListField(default=[], read_only=True)
    # comments = CommentsSerializer()
    # likes = LikesSerializer()
    published = serializers.DateTimeField()
    visibility = serializers.CharField()

    '''
    The following three functions were made with the help of:

    ChatGPT with prompt: "How can i change this post serializer so it will dynamically allocate content type based on the type of image."
    Date Accessed: 2024-11-03
    '''
    def get_contentType(self, obj):
        if obj.content_type == "IMAGE":
            # Convert memoryview to bytes if necessary
            image_data = obj.content.tobytes() if isinstance(obj.content, memoryview) else obj.content
            # Determine image type (e.g., png, jpeg)
            image_type = imghdr.what(None, h=image_data)
            if image_type == "jpeg":
                return "image/jpeg;base64"
            else:
                return "image/png;base64"
            # HACK application/base64s won't display as images in browsers, so just default to png
            # Brett: I don't know why gold's images detect as app/base64, but we work with it
            # else:
            #     return "application/base64"
        return obj.content_type  # Use the content type from the model for non-images

    def get_content(self, obj):
        if obj.content:
            if obj.content_type == "IMAGE":
                # Handle memoryview conversion for base64 encoding
                image_data = obj.content.tobytes() if isinstance(obj.content, memoryview) else obj.content
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                print("||||||||||||||||||||||||IMAGE BASE 64||||||||||||||||||||||||||")
                f = self.get_contentType(obj)
                print(f"data:{f},{image_base64}")
                image = f"data:{f},{image_base64}"
                return image
            return obj.content
        return None

    def validate_content(self, value):
        content_type = self.initial_data.get('content_type', None)
        print(type(value))
        if content_type == "IMAGE":
            if isinstance(value, str):
                print("In string")
                try:
                    # Remove data URL prefix if present
                    if value.startswith('data:'):
                        value = value.split('base64,')[1]
                    return base64.b64decode(value)
                except Exception as e:
                    raise serializers.ValidationError(f"Invalid base64 image data: {str(e)}")
            elif isinstance(value, (bytes, memoryview)):
                print("In string")
                # Binary content is directly valid for IMAGE
                return value
            else:
                raise serializers.ValidationError("Invalid content format for IMAGE. Expected base64 string or binary data.")
        return value

    # def get_comments(self, obj):
    #     comments = Comment.objects.filter(serial=obj.post)
    #     comments = comments[0:min(5, len(comments))]
    #     serializer = CommentsSerializer(comments)

    def update(self, instance, validated_data):
        print("in update")
        # update existing post instance with validated_data
        instance.visibility = validated_data.get("visibility",
                                                 instance.visibility)
        instance.content = validated_data.get("content",
                                              instance.content)
        instance.description = validated_data.get("description",
                                                  instance.description)
        instance.title = validated_data.get("title",
                                            instance.title)
        instance.contentType = 'image/jpeg;base64'
        instance.save()
        return instance

    def create(self, validated_data):
        print("in Create")
        # Create Author Object
        author_data = validated_data.pop('author')
        author = Author.objects.get(fqid=author_data['fqid'])

        # Create the Post Object using the Author Object
        post = Post.objects.create(author=author, **validated_data)
        contentType = 'image/jpeg;base64'
        return post, contentType



class PostsSerializer(serializers.Serializer):
    type = serializers.CharField(default="post", read_only=True)
    page_number = serializers.IntegerField()
    size = serializers.IntegerField()
    count = serializers.IntegerField()
    src = PostSerializer(many=True, read_only=True)
