# from tastypie.resources import Resource
 
# from .models import Post
 
# class AjaxSearchResource(Resource):
 
#     class Meta:
#         resource_name = 'ajaxsearch'
#         allowed_methods = ['post']
 
#     def post_list(self, request, **kwargs):
#         phrase = request.POST.get('q')
#         if phrase:
#             posts = list(Post.objects.filter(title__icontains=phrase).values('id', 'title'))
#             return self.create_response(request, {'posts': posts})
