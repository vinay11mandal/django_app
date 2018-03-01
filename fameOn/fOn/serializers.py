from rest_framework import serializers
from datetime import datetime
from .models import Post

class PostSerializer(serializers.ModelSerializer):
	publish = serializers.Field(source = 'convert_to_dt')
	created = serializers.Field(source = 'convert_to_dte')
	#//and need to write the convert_to_dt method in Post model// below method 
	# publish = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False, read_only=True)
	# created = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False, read_only=True)
	class Meta:
		model = Post	
		fields = ('body', 'user_posted', 'publish', 'created', 'userpost')
		read_only_fields = ('publish', 'created')

		def create(self, validated_data):
			body = validated_data.get('body', None)
			user_post = validated_data.get('user_post')
			publish = validated_data.get('date', None)
			created = validated_data.get('created', None)
			userpost = validated_data.get('user')
			return Post.objects.create(body=body, user_post = user_post, publish=publish, created=created, userpost=userpost)
