from django.urls import path
from . import views
from .views import BlogCreate, BlogUpdate, BlogDelete, BlogList
# blogs
urlpatterns = [
     path('', views.index, name='latest_blogs'),
     path('my_blogs/', views.my_blogs, name='my_blogs'),
     path('my_blogs/my_blog_search', views.my_blogs_search, name='my_blogs_search'),
     path('drafts/', views.drafts, name='drafts'),
     path('blog/<int:pk>', views.blog, name='blog'),
     # path('blog/<int:pk>/comment/', views.add_comment, name='add_comment'),

     path('blog/<int:blog_id>/comment/update/<int:comment_id>',
          views.comment_update, name='comment_update'),
     path('blog/<int:blog_id>/comment/delete/<int:comment_id>',
          views.comment_delete, name='comment_delete'),

     path('create/', BlogCreate.as_view(), name='blog_create'),
     path('update/<int:pk>/', BlogUpdate.as_view(), name='blog_update'),
     path('delete/<int:pk>/', BlogDelete.as_view(), name='blog_delete'),
     path('all_blogs/', BlogList.as_view(), name='all_blogs'),
     path('all_blogs/all_blogs_search/',
          views.all_blogs_search, name='all_blogs_search'),
     path('tag_redirect', views.tag_redirect, name='tag_redirect')
]
