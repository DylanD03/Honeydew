from django.contrib import admin
from .models import Post, Author, Follow, Friendship, Like, Node, LocalUser, Comment, Colours

# Customizing our Admin Panel

class PostAdmin(admin.ModelAdmin):
  list_display = ['title', 'author', 'fqid']

class AuthorAdmin(admin.ModelAdmin):
  list_display = ['display_name', 'fqid']

class FollowAdmin(admin.ModelAdmin):
  list_display = ['following', 'follower']

class FriendshipAdmin(admin.ModelAdmin):
  list_display = ['author1', 'author2']

class LikeAdmin(admin.ModelAdmin):
  list_display = ['author', 'post' ,'fqid']

class NodeAdmin(admin.ModelAdmin):
  list_display = ['host', 'enable_connection']

class CommentAdmin(admin.ModelAdmin):
  list_display = ['author', 'post', 'fqid', 'content']

# Specify which tables we can see/edit from our Admin panel
admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(LocalUser)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Colours)