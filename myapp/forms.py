# from django importing forms
from django import forms

# importing models
from models import UserModel,PostModel,LikeModel,CommentModel

# creating SignUpForm
class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields=['email','username','name','password']

# creating LoginForm
class LoginForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password']

# creating PostForm
class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields=['image', 'caption']

# creating LikeForm
class LikeForm(forms.ModelForm):

    class Meta:
        model = LikeModel
        fields=['post']

# creating CommentForm
class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment_text', 'post']

# creating Upvote Form
class UpvoteForm(forms.Form):
    id = forms.IntegerField()

# creating SearchForm
class SearchForm(forms.Form):
    searchquery = forms.CharField();
















