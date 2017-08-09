# importing db
from django.contrib.sessions.backends import db

# importing models
from django.db import models

#importing uuid
import uuid

# Creating UserModel
class UserModel(models.Model):

#email field
	email = models.EmailField()

#name field
	name = models.CharField(max_length=120)

# username field
	username = models.CharField(max_length=120)

# password field
	password = models.CharField(max_length=40)

# created on field
	created_on = models.DateTimeField(auto_now_add=True)

# updated on field
	updated_on = models.DateTimeField(auto_now=True)

# creating SessionToken Model
class SessionToken(models.Model):
	user = models.ForeignKey(UserModel)

# session token field
	session_token = models.CharField(max_length=255)

# last request field
	last_request_on = models.DateTimeField(auto_now=True)

# created on field
	created_on = models.DateTimeField(auto_now_add=True)

# is valid field
	is_valid = models.BooleanField(default=True)

# create_token function
	def create_token(self):
		self.session_token = uuid.uuid4()

# creating PostModel
class PostModel(models.Model):
	user = models.ForeignKey(UserModel)
	image = models.FileField(upload_to='user_images')

# image_url field
	image_url = models.CharField(max_length=255)

# caption field
	caption = models.CharField(max_length=240)

# created on field
	created_on = models.DateTimeField(auto_now_add=True)

# updated on field
	updated_on = models.DateTimeField(auto_now=True)
	has_liked = False

# property for like_count
	@property
	def like_count(self):
		return len(LikeModel.objects.filter(post=self))

#property for comments
	@property
	def comments(self):
		return CommentModel.objects.filter(post=self).order_by('-created_on')

# creating LikeModel
class LikeModel(models.Model):
	user = models.ForeignKey(UserModel)
	post = models.ForeignKey(PostModel)


# created on field
	created_on = models.DateTimeField(auto_now_add=True)

# updated on field
	updated_on = models.DateTimeField(auto_now=True)

# creating CommentModel
class CommentModel(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    upvote_num = models.IntegerField(default=0)

# comment text field
    comment_text = models.CharField(max_length=555)

# created on field
    created_on = models.DateTimeField(auto_now_add=True)

# updated on field
    updated_on = models.DateTimeField(auto_now=True)


