import base64
import socket
from django.conf import settings  # Import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response

from honeydew.models import Node
from stream.views import friends_list


HTTP = "https://"
SITE = Site.objects.get_current


def get_owner_friend(request, author):
    owner = False
    friend = False
    if request.user.is_authenticated:
        if request.user.author.fqid == author.fqid:
            owner = True
        elif request.user.author.fqid in friends_list(author.fqid):
            friend = True

    return owner, friend


def encode_basic_auth(username, password):
    """
    Encodes the username and password for Basic Authentication.
    Used to convert the Authorization header from
    "Basic username:password" into "Basic <encoded string>"
    
    Input:
        username (str): The username
        password (str): The password
    
    Returns:
        str: The encoded Basic Auth value.
        example: "Basic YXNsa2Rmajppb2pkYWZh"
    
    Credit: https://stackoverflow.com/a/56881185
    """
    auth = f"{username}:{password}"
    encoded_auth = base64.b64encode(auth.encode('utf-8')).decode('utf-8')
    return f"Basic {encoded_auth}"



class CustomAuthentication(BaseAuthentication):
    """
      Overriding Authentification. Only allow specific Username/Password
      To Authenticate, rather than using any user object, which is the default django behaviour.
      Source: https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication

      Must Authenticate by using the "Authorization" Header
      'Authorization': "Basic username:password"
        username is replaced by the authentification username
        password is replaced by the authentification password
        And the username:password is a Base64 Encoded String
      For Example:
        'Authorization': "Basic YXNsa2Rmajppb2pkYWZh"
    """
    def authenticate_header(self, request):
      """
        Returns a header indicating why Authentification failed.
        Explains how to authenticate properly.
      """
      return f"To authenticate, provide Authorization: Basic Username:Password in the Header. Where Username:Password is Base64 Encoded."


    def authenticate(self, request):
      """
        From Source: https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
        To implement a custom authentication scheme, subclass BaseAuthentication 
        and override the .authenticate(self, request) method. 

        Many of the Comments below are taken directly from source, to indicate where the code came from
      """
      print("**** IN AUTHENTICATE ****")
      # Get the Authorization header
      auth = request.META.get('Authorization') or request.META.get('HTTP_AUTHORIZATION')
      host = request.get_host()

      print(auth, ": auth", host, ": host")


      # If authentication is not attempted, return None. Any other authentication schemes also in use will still be checked.
      if not auth:
        print("Authorization header missing.")
        raise AuthenticationFailed('Authorization header missing.')

      # Check if the header is in the correct Basic format
      if (auth[0:6] != 'Basic '):
        print('Authorization header must start with Basic.')
        raise AuthenticationFailed('Authorization header must start with Basic.')

      # Extract the base64 encoded credentials part
      auth_credentials = auth[6:]  # Remove "Basic " from the string

      try:
        # Decode the base64 string to get "username:password"
        # Credit: "How to Decode Basic Auth in python" from chatGPT
        decoded_credentials = base64.b64decode(auth_credentials).decode('utf-8')
        our_username, our_password = decoded_credentials.split(':', 1)  # Split on first colon

      except:
        print('Invalid Authorization header format.')
        raise AuthenticationFailed('Invalid Authorization header format.')

      # Check if the username and password match the specific values
      node = Node.objects.filter(our_username=our_username, our_password=our_password).first()
      if not node:
        print("Node not found.")
        raise AuthenticationFailed("Node not found.")
      print("node", node)
      
      # Check if host is enabled      
      if not node.enable_connection:
        # 8.07 I want to be able to remove nodes and stop sharing with them
        # 8.10 I can disable the node to node interfaces for connections that I no longer want
        print("Connections to this node are disabled.")
        raise AuthenticationFailed("Connections to this node are disabled.")
      
      # Authenticate and return the user
      User = get_user_model()
      user, _ = User.objects.get_or_create(username=our_username)
      return (user, None)  # Return the authenticated user and None (no token)
    











"""
  FUNCTIONS FOR TESTING ONLY
"""
# This API authenticates users who use the correct username/password.
# https://www.geeksforgeeks.org/basic-authentication-django-rest-framework/
@api_view(['GET']) 
@authentication_classes([CustomAuthentication])  # Apply custom authentication here
@permission_classes([IsAuthenticated]) 
def authenticate(request, format=None): 
    """
      Must Authenticate by using the "Authorization" Header
        'Authorization': "Basic username:password"
              username is replaced by the authentification username
              password is replaced by the authentification password
              And the username:password is a Base64 Encoded String
      For Example:
        'Authorization': "Basic YXNsa2Rmajppb2pkYWZh"
    """
    # Return Authenticated user info
    content = {         
        'user': str(request.user), 
        'auth': str(request.auth), 
    } 
    return Response(content) 

# Get request does not require Authentication
@api_view(['GET']) 
def test_authenticate(request, format=None): 
    
    """
    GET request does not Authentication

    THIS CLASS IS ONLY FOR TESTING PURPOSES.
    Also serves as a template on how to use Django's HTTP Basic authentification
    Read More: https://www.geeksforgeeks.org/basic-authentication-django-rest-framework/
    """

    return Response(200)

# Post request requires Authentication
@api_view(['POST']) 
@authentication_classes([CustomAuthentication])  # Apply custom authentication here
@permission_classes([IsAuthenticated]) 
def test_authenticate(request, format=None): 
    """
    Post request DOES require Authentication

    THIS CLASS IS ONLY FOR TESTING PURPOSES.
    Also serves as a template on how to use Django's HTTP Basic authentification
    Read More: https://www.geeksforgeeks.org/basic-authentication-django-rest-framework/

    Must Authenticate by using the "Authorization" Header
      'Authorization': "Basic username:password"
        username is replaced by the authentification username
        password is replaced by the authentification password
        And the username:password is a Base64 Encoded String
    For Example:
      'Authorization': "Basic YXNsa2Rmajppb2pkYWZh"
    """
    return Response(request.data)
