
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.models import Group 
admin.site.site_title = 'カロリー＆PFCバランス管理サイト'
admin.site.site_header = 'カロリー＆PFCバランス管理サイト'
admin.site.index_title = 'カロリー＆PFCバランス管理サイト'
# admin.site.disable_action('delete_selected')

urlpatterns = [
    path('', include('base.urls')),
    path('blogs/', include('blog.urls')),
    path('account/', include('account.urls')),
    # path('admin/', admin.site.urls),
]
