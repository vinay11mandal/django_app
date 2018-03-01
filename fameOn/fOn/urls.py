from django.conf.urls import url, include
from allauth.account import views as allauth_views
from . import views

app_name = 'fOn'
urlpatterns = [
		url(r'^home', views.home, name = 'home'),
		url(r'^show_posts', views.show_posts, name = 'show_posts'),
		url(r'^signup/$', allauth_views.signup, name="account_signup"),
		url(r'^accounts/logout', allauth_views.login, name = 'account_logout'),
		url(r'^profile', views.profile, name = 'profile'),
		url(r'^delete_post',views.delete_post, name = 'delete_post'),
		url(r'^create_post/$', views.create_post, name = 'create_post'),
		url(r'^comment/$', views.comment, name = 'comment'),
		url(r'^show_comments', views.show_comments, name = 'show_comments'),
		url(r'^delete_comment', views.delete_comment, name = 'delete_comment'),
		url(r'^unlikepost/$', views.unlikePost, name = 'unlikepost'),
		url(r'^likepost/$', views.likePost, name = 'likepost'),
		url(r'^upload_image', views.upload_image, name='upload_image'),
		url(r'^get_user_detail', views.get_user_detail, name='get_user_detail'),
		url(r'^search', views.search, name='search'),
		url(r'^personal_information', views.personal_information, name='personal_information'),
		url(r'^edit_personal_info', views.edit_personal_info, name='edit_personal_info'),
		]
