# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.signals import post_save
from django.utils import timezone

# def upload_location(instance, filename):
# 	return "%s/%s" %(instance.id, filename)

class UserDetail(models.Model):
	
	TITLE_CHOICES = (
				('MR', 'Mr.'),
				('MRS', 'Mrs.'),
				('MS', 'Ms,'),
	)
	GENDER_CHOICES = (
		('F', 'Female',),
		('M', 'Male',),
		('O', 'Other',),
	)
	
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	title = models.CharField(max_length = 3, choices = TITLE_CHOICES,)
	gender = models.CharField(max_length = 1, choices = GENDER_CHOICES,)
	mobile = models.IntegerField()
	email = models.EmailField(max_length = 254)
	user = models.OneToOneField(User, null=True, blank=True, on_delete = models.CASCADE)
	friends = models.ManyToManyField('self')

# Creating association between User And Userdetail using signal's post_save method
	def create_profile(sender, **kwargs):
		if kwargs['created']:
			user_profile = UserDetail.objects.create(user=kwargs['instance'])
	post_save.connect(create_profile, sender=User)

	def __str__(self):
		return self.first_name

class ProfilePicture(models.Model):
	user = models.OneToOneField(User, null=True, blank = True, on_delete = models.CASCADE)
	created_date = models.DateTimeField(default = timezone.now)
	profile_picture = models.ImageField(upload_to ='media/', default = 'media/image1.jpeg',blank=True, null=True)

class Post(models.Model):
	title = models.TextField(max_length = 100, blank = True, null = True)
	body = models.TextField(max_length = 254)
	user_posted = models.CharField(max_length = 254, blank = True, null = True)
	publish = models.DateTimeField(default = timezone.now)
	published = models.BooleanField(default = False)
	created = models.DateTimeField(auto_now_add = True)
	userpost = models.ForeignKey(User, blank = True, null = True)

	def approve(self):
		self.published = True
		self.save()
	
	def convert_to_dt(self):
		result = self.publish.strftime('%y-%m-%d %H:%M')
		return result

	def convert_to_dte(self):
		result = self.created.strftime('%y-%m-%d %H:%M')
		return result
		
	def __str__(self):
		return self.body

class Comment(models.Model):
	text = models.TextField(max_length = 254)
	created_date = models.DateTimeField(default = timezone.now)
	user_commented = models.CharField(max_length = 256, blank = True, null = True)
	approved_comment = models.BooleanField(default = False)
	post = models.ForeignKey(Post, blank = True, null = True)
	usercomment = models.ForeignKey(User, blank = True, null = True)

	def approve(self):
		self.approved_comment = True
		self.save()
	
	def __str__(self):
		return self.text

class Like(models.Model):
	liked_date = models.DateTimeField(auto_now_add = True)
	liked_count = models.SmallIntegerField(default = 0)
	liked_post = models.ForeignKey(Post, blank = True, null = True)
	userlike = models.ForeignKey(User, blank = True, null = True)
	
	def __str__(self):
		return '%s' % self.liked_post

	def total_likes(self):
		return self.liked_post.like_set.count()

class Unlike(models.Model):
	unliked_date = models.DateTimeField(auto_now_add = True)
	unliked_count = models.SmallIntegerField(default = 0)
	unliked_post = models.ForeignKey(Post, blank = True, null = True)
	userunlike = models.ForeignKey(User, blank = True, null = True)

	def __str__(self):
	   return self.unliked_post

	def total_unlikes(self):
		return self.unliked_post.unlike_set.count()

class Friend(models.Model):
	name = models.CharField(max_length = 256, blank = True, null = True)
	user = models.ForeignKey(User, blank=True, null=True)
	user_detail = models.ForeignKey(UserDetail, blank=True, null=True)