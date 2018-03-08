# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from fOn.forms import SignupForm, PostForm, ProfilePicForm
from allauth.account.views import signup, login
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
import json
from json import dumps, loads, JSONEncoder, JSONDecoder
from django.core import serializers
from .models import UserDetail, Post, Comment, Like, Unlike, ProfilePicture  
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
import datetime
from fOn.utils import decode_base64_file

def welcome(request):
    return render_to_response('fOn/welcome.html')

@login_required
def home(request):
    form = PostForm()
    return render(request, 'fOn/home.html', {'form':form})

@login_required
def show_posts(request):
    post = Post.objects.all().order_by('-created')
    like = Like.objects.all()
    if post:
        case_list = []
        data = {}
        for each in post:
            data['id']=each.id
            data['body']=each.body
            data['user_posted']=each.user_posted
            data['created']=each.publish.strftime('%y-%m-%d %H:%M')
            data['like']=each.like_set.count()
            case_list.append(data.copy())
    list_data = {'post':list(case_list)}
    return HttpResponse(json.dumps(list_data), content_type="application/json")

@csrf_exempt
@login_required
def show_comments(request):
    post_id = request.POST.get('post_id')
    if Comment.objects.filter(post = post_id).exists():
        comment = Comment.objects.filter(post=post_id)
        my_list = []
        data={}
        for each in comment:
            data['text'] = each.text
            data['created_date'] = each.created_date.strftime('%y-%m-%d %H:%M')
            data['comment_id'] = each.id
            data['user_commented'] = each.user_commented
            my_list.append(data.copy())        
        list_data = {'comment':list(my_list), 'post_id':post_id}
        return HttpResponse(json.dumps(list_data), content_type="application/json")
    list_data = {'post_id':post_id}
    return HttpResponse(json.dumps(list_data), content_type="application/json")

@login_required
@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        post_text = request.POST.get('post')
        user = request.user
        post = Post.objects.create(body = post_text, user_posted = request.user, userpost = user)
        data = {
            'post_id': post.id,
            'post': post.body,
            'publish': post.publish.strftime('%Y-%m-%d %H:%M'),
            'author':  post.userpost.get_full_name(),
        }
        return HttpResponse(json.dumps(data),content_type = "application/json")
    else:
        return HttpResponse(json.dumps({"nothing": "this isn't happening"}),content_type = "application/json")

@login_required
@csrf_exempt
def comment(request):
    if request.method == 'POST':
        post = request.POST.get('post')
        comment_text = request.POST.get('comment')
        post_id = Post.objects.get(id=post)
        comment = Comment.objects.create(user_commented = request.user, text = comment_text, usercomment = request.user, post = post_id)
        data = {
            'comment_id': comment.id,
            'comment_text': comment.text,
            'comment_date': comment.created_date.strftime('%y-%m-%d %H:%M'),
            'usercomment': comment.usercomment.get_full_name(), 
        }
        return HttpResponse(json.dumps(data),content_type = "application/json")
    else:
        return HttpResponse(json.dumps({'nothing':"this isn't happening"}), content_type = "application/json")

@login_required
def profile(request):
    return render(request, 'fOn/profile.html')

@login_required
def likePost(request):
    post_id = request.GET.get('post_id')
    if post_id:
        likedpost = Post.objects.get(pk=post_id)
        if not Like.objects.filter(liked_post = likedpost, userlike=request.user).exists():
            instance = Like(liked_post=likedpost, userlike=request.user)
            instance.save()
            data = {'likes_count': likedpost.like_set.count()}
            return HttpResponse(json.dumps(data), content_type = 'application/json')
        else:
            data = {'likes_count': likedpost.like_set.count(), 'message':"Already liked"}
            return HttpResponse(json.dumps(data), content_type = 'application/json')

@login_required
def unlikePost(request):
    post_id = request.GET.get('post_id')
    if post_id:
        unlikedpost = Post.objects.get(pk=post_id)
        like = Like.objects.filter(liked_post = unlikedpost, userlike=request.user)
        if like:
            like[0].delete()
            data = {'likes_count': unlikedpost.like_set.count()}
            return HttpResponse(json.dumps(data), content_type = 'application/json')
        else:
            data = {'likes_count': unlikedpost.like_set.count(), 'message': "Already unliked"}
            return HttpResponse(json.dumps(data), content_type = 'application/json')   

@login_required
def delete_post(request):
    post_id = request.GET.get('post_id')
    if post_id:
        post = Post.objects.filter(id =int(post_id), userpost=request.user)
        if post:
            post[0].delete()
            data = {'message': "Post deleted"}
            return HttpResponse(json.dumps(data), content_type = 'application/json')
        data = {'message': "Action isn't perform"}
        return HttpResponse(json.dumps(data), content_type = 'application/json')

@login_required
def delete_comment(request):
    comment_id = request.GET.get('comment_id')
    if comment_id:
        comment = Comment.objects.filter(id = int(comment_id), user_commented = request.user)
        if comment:
            comment[0].delete()
            data = {'message': "Comment deleted"}
            return HttpResponse(json.dumps(data), content_type = "application/json")      
        data = {'message': "Action isn't perform"}
        return HttpResponse(json.dumps(data), content_type = "application/json")

#Searching name
@csrf_exempt
def get_user_detail(request):
    if request.method == 'POST':
        q = request.POST['search_text']
    else:
        q = ''
    name = UserDetail.objects.filter(
            Q(first_name__icontains = q)| 
            Q(last_name__icontains = q)).distinct()[:10]
    return render_to_response('fOn/ajax-search.html', {'name':name})

@csrf_exempt
def search(request):
    if request.method == 'POST':
        q = request.POST['search_text']
    else:
        q = ''
    # name = UserDetail.objects.filter(
    #         Q(first_name__icontains = q)| 
    #         Q(last_name__icontains = q)).distinct()[:10]
    name = UserDetail.objects.filter(Q(first_name__icontains = q)).distinct()[:10]
    # data = {}
    # search_list = []
    # for itr in name:
    #     data['name'] = itr.first_name,
    #     search_list.append(data.copy())
    # data = {"name": list(search_list)}
    data = json.dumps(list(name))
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
@csrf_exempt
def personal_information(request):
    if request.method == 'POST':
        instance = UserDetail.objects.get(id = request.user.id)
        data = {
            "first_name": instance.first_name, 
            "last_name": instance.last_name,
            "title": instance.title,
            "gender":instance.gender,
            "email":instance.email,
            "phone":instance.mobile,}
        return HttpResponse(json.dumps(data), content_type="application/json")
    data = {"message": "Personal information"}
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
@csrf_exempt
def edit_personal_info(request):
    if request.method == 'POST':
        if UserDetail.objects.filter(id =request.user.id).exists():
            dic = json.loads(request.body)
            UserDetail.objects.filter(pk = request.user.pk).update(**dic)
            data = {"response": "data updated"}
            return HttpResponse(json.dumps(data), content_type="application/json")
    data = {"response": "data is not edited"}
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def upload_image(request):
    ProfilePicture.objects.create(profile_picture = request.FILES['mypicture'])
    # if ProfilePicture.objects.filter(user = request.user).exists():
    #     ProfilePicture.objects.get(id = request.user).profile_picture.delete(save=True)
    #     ProfilePicture.objects.get(id = request.user.id, picture_profile= request.FILES['mypicture']) 
    #     data = {"message": "image updated successfully"}
    #     return  HttpResponse(json.dumps(data), content_type = 'application/json')
    # else:
    #     ProfilePicture.objects.create(user = request.user, profile_picture = request.FILES['mypicture'])
    #     data = {"message": "image uploaded successfully"}
    #     return HttpResponse(json.dumps(data), content_type = 'application/json')
    data = {"message": "Error while uploading image, please try later!!"}
    return HttpResponse(json.dumps(data), content_type = 'application/json')

# image upload when image submited using modelform

# @csrf_exempt
# def upload_image(request):
#   if request.method == 'POST':

#       form =  ProfilePicForm(request.POST or None, request.FILES or None)
#       # handle_uploaded_file(request.FILES['profile_picture'])
#       if form.is_valid():
#           instance = form.save()
#           instance.user = request.user
#           ins = instance.save()
#           image = ins
#       context = {'success': "image uploaded", 'profile_picture': image}
#       return render(request, 'fOn/home.html', context)

#\\\\\ image submitted through onchane using base64

# import base64
# import cStringIO
# from django.core.files.base import ContentFile
# from django.core.files import File
# @csrf_exempt
# def upload_image(request):
#     img = request.POST.get('img')
#     if request.method == "POST":
#         image = decode_base64_file(img)
        
#         ProfileImage.objects.create(user = request.user, profile_picture=image)       
#         data = {"message": "image saved sucessfully"}
#         return HttpResponse(json.dumps(data), content_type='application/json')
#     return HttpResponse(json.dumps(data), content_type='application/json') 

#posts
class PostList(APIView):

    def get(self, request):
        post = Post.objects.all().order_by('-created')
        serializer  = PostSerializer(post, many=True)
        return response(serializer.data)

    def post(self, request):
        user = request.user
        serializer  = PostSerializer(post, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
