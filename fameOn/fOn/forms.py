
from fOn.models import UserDetail, Post, Comment, ProfilePicture
from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
     
    class Meta:
        model = UserDetail
        fields = ('first_name', 'last_name','title', 'gender', 'mobile', 'email')
    
    def signup(self, request, user):
        # Saving your user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # Saving the UserDetails
        userdetail = UserDetail()
        userdetail.user = user
        userdetail.title = self.cleaned_data['title']
        userdetail.gender = self.cleaned_data['gender']
        userdetail.mobile = self.cleaned_data['mobile']
        userdetail.email = self.clean_data['mobile']
        userdetail.save()

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs=
                { 'id':'post-text','cols': 60, 'rows': 3, 'required': True,'placeholder': 'Write your post...'}),}

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = ProfilePicture
        fields = ('profile_picture',)
                            