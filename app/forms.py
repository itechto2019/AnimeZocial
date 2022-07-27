from django.forms import FileInput, ModelForm, TextInput, Textarea
from . models import Feed, Like, Comment
from django.contrib.auth.models import User

class FeedForm(ModelForm):
    class Meta:
        model = Feed
        fields = "__all__"
        exclude = ['user','likes', 'comments']
        widgets  = {
            'body' : Textarea(attrs={'placeholder': 'Share anything...'})
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'first_name', 'last_name']
        widgets  = {
            'username' : TextInput(attrs={'placeholder': 'Username'}),
            'email' : TextInput(attrs={'placeholder': 'Email address'}),
            'first_name' : TextInput(attrs={'placeholder': 'Firstname'}),
            'last_name' : TextInput(attrs={'placeholder': 'Lastname'}),
        }

class LikeForm(ModelForm):
    class Meta:
        model = Like
        fields = '__all__'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['user','feed']
        widgets = {
            'body' : TextInput(attrs={
                'placeholder' : 'Write your comment',
                'style' : 'padding: 10px;'
            })
        }

