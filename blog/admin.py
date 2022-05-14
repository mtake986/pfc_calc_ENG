from django.contrib import admin
from .models import Blog, Comment
# Register your models here.
class BlogAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'user', 'is_public', 'created', 'updated', 'tag_list')
  list_display_links = ('id',)
  list_filter = ('user', 'is_public')
  search_fields = ('title',)
  list_per_page = 50
  def get_queryset(self, request):
    return super().get_queryset(request).prefetch_related('tags')

  def tag_list(self, obj):
      return u", ".join(o.name for o in obj.tags.all())
admin.site.register(Blog, BlogAdmin)

class CommentAdmin(admin.ModelAdmin):
  list_display = ('id', 'text',)
admin.site.register(Comment, CommentAdmin)