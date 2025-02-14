from django.shortcuts import render, redirect
from .models import Author, LocalUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from flags.state import flag_enabled


def login_page(request):
    # if user is already logged in -> just redirect to home
    # and user is attached to an author (admins are not authors)
    if request.user.is_authenticated and request.user.author:
        return redirect('stream-home')
    return render(request, "login.html")


def logoutRequest(request):
    logout(request)
    return redirect("login")


def submit_login_credentials(request):
    entered_username = request.POST.get('username')
    entered_password = request.POST.get('password')
    user = authenticate(username=entered_username, password=entered_password)

    if user is not None:
        # user found
        login(request, user)
        return redirect('stream-home')
    # if user is not found, display error on next page
    messages.error(request, "Username or Password does not match")
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")


def submit_signup_credentials(request):
    entered_password = request.POST.get('password')
    confirm_password = request.POST.get('password-confirm')
    # ensure passwords match
    if (entered_password != confirm_password):
        messages.error(request, "Passwords do not match!")
        # passwords dont match -> refresh signup page to do it again
        return render(request, "signup.html")

    entered_username = request.POST.get('username')
    # Enforce unique usernames??
    if LocalUser.objects.filter(username=entered_username).exists():
        messages.error(request, "Username already taken")
        return render(request, "signup.html")

    # create and save user immediately if admin verification is off
    author = Author.objects.create(
        display_name=entered_username,
        local = True
    )
    author.save()

    user = LocalUser.objects.create_user(
        username=entered_username,
        password=entered_password,
        author=author,
        is_active=not flag_enabled("ADMIN_VERIFICATION")
    )
    user.save()

    return redirect('login')  # return user to signup page so they can use new creds
