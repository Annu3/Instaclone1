# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import Comment
from tokenize import Comment

# import render and redirect from django.shortcuts
from django.shortcuts import render, redirect

# importing SignUpForm,LoginForm,PostForm,LikeForm,CommentForm,UpvoteForm,SearchForm from forms
from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm, UpvoteForm, SearchForm

# importing UserModel, SessionToken, PostModel, LikeModel, CommentModel from models
from models import UserModel, SessionToken, PostModel, LikeModel, CommentModel

# importing make_password and check_password function
from django.contrib.auth.hashers import make_password, check_password

# importing BASE_DIR from settings
from insta_clone.settings import BASE_DIR

# importing ImgurClient from imgurpython
from imgurpython import ImgurClient

#importing get_api_key from paralleldots.config
from paralleldots.config import get_api_key

# importing timedelta and datetime from datetime
from datetime import timedelta, datetime

# importing timezone
from django.utils import timezone

# importing requests
import requests

# importing json
import json

# creating signup_view function
def signup_view(request):

# requesting POST method
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

# saving data to DB
            empty = len(username) == 0 and len(password) == 0
            if len(username) >= 4 and len(password) >= 3:
                user = UserModel(name=name, password=make_password(password), email=email, username=username)
                user.save()

# rendering the page to success.html
                return render(request, 'success.html')
            text = {}
            text = "Username or password is not long enough"

# return redirect('login/')
        else:
            form = SignUpForm()
    elif request.method == "GET":
        form = SignUpForm()
        today = datetime.now()
    return render(request, 'index.html', {'today': today, 'form': form})

    return render(request, 'index.html', {'form': form})

# creating login_view function
def login_view(request):
    response_data = {}

# requesting POST method
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

# checking password
            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html', response_data)

# creating like_view function
def like_view(request):

# checking if user is valid
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            posts = PostModel.objects.all().order_by('-created_on')
            for post in posts:

                existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

                if existing_like:
                    post.has_liked = True

                if not existing_like:
                    LikeModel.objects.create(post_id=post_id, user=user)
                else:
                    existing_like.delete()

                return redirect('/feed/')

        else:
            return redirect('/feed/')

    else:
        return redirect('/login/')

# creating feed_view function
def feed_view(request):

# checking if user is valid
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('created_on')
        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')

# creating post_view function
def post_view(request):

# checkinng if user is valid
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + "\\" + post.image.url)

                client = ImgurClient('b05a87fc2d9b16a', 'e40bae7fc06026074022bcac6b4f370fe4963cba')
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()

                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')


# creating comment_view function
def comment_view(request, comment_text=None):

#objective for review of positive or  negative  comment
#set api_key
    api_key = "39JDDYmgIv5c1FPr54X0ozcQ6L8nnk29DejqgZ2h7aY"
    req_json = None

# 1 is for positive comment and 0 is for negative comment
    try:
        req_json = requests.post.json()
        if req_json is not None:
             sentiment = req_json['sentiment']
             print req_json
             print req_json['confidence_score']
             if req_json['sentence_type'] == "Positive Comment":

#if comment is positive it is greater than 5 percent
                if req_json['confidence_score'] > 5:

#return positive comment
                   return 1
                else:

#return negative comment
                    return 0
             else:
                    return 0
    except:
                    return 0
#url for the parallel dots of sentiment
    url = "http://apis.paralleldots.com/sentiment"

# function to check if user is valid
    user = check_validation(request)

#check user exists and request post
    if user and request.method == 'POST':
       form = CommentForm(request.POST)

#check if form is valid
       if  form.is_valid():

#retrieve post id
            post_id = form.cleaned_data.get('post').id

#accept comment text from the form
            comment_text = form.cleaned_data.get('comment_text')

            r = requests.get(url, params={"apikey": api_key, "comment": comment_text})
            print r
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)

#comment save
            comment.save()

#redirect to the feed page
            return redirect('/feed/')
       else:
            return redirect('/feed/')
    else:
        return redirect('/login/')

#creating check_validation function
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None

# creating logout_view function
def logout_view(request):

#checking if user is valid
    user = check_validation(request)

    if user is not None:
        latest_sessn = SessionToken.objects.filter(user=user).last()
        if latest_sessn:
            latest_sessn.delete()

#redirecting to login
            return redirect("/login/")


# creating upvote_view function for comments
def upvote_view(request):
    user = check_validation(request)
    comment = None

    print ("upvote view")
    if user and request.method == 'POST':

        form = UpvoteForm(request.POST)
        if form.is_valid():

            comment_id = int(form.cleaned_data.get('id'))

            comment = CommentModel.objects.filter(id=comment_id).first()
            print ("upvoted not yet")

            if comment is not None:

# print unliking post
                print ("upvoted")
                comment.upvote_num += 1
                comment.save()
                print (comment.upvote_num)
            else:
                print ('stupid mistake')

        return redirect('/feed/')
    else:
        return redirect('/feed/')

# creating query_based_search_view function
def query_based_search_view(request):

# checking if user is valid
    user = check_validation(request)
    if user:
        if request.method == "POST":
            searchForm = SearchForm(request.POST)
            if searchForm.is_valid():
                print 'valid'
                username_query = searchForm.cleaned_data.get('searchquery')
                user_with_query = UserModel.objects.filter(username=username_query).first();
                posts = PostModel.objects.filter(user=user_with_query)
                return render(request, 'feed.html', {'posts': posts})

            else:
                return redirect('/feed/')
    else:
        return redirect('/login/')