from django.contrib import admin
from .models import Food, Target, Favorite
# Register your models here.

class FoodAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'user', 'category', 'kcal', 'protein', 'fat', 'carb', 'eaten_date')
  list_display_links = ('id',)
  list_filter = ('name', 'category')
  # list_editable = ('category', 'kcal', 'protein', 'fat', 'carb')
  search_fields = ('name', 'category')
  list_per_page = 50

class TargetAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'kcal', 'protein', 'fat', 'carb')
  list_display_links = ('id', 'user')
  list_filter = ('user',)
  search_fields = ('user',)
  list_per_page = 50

class FavoriteAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'kcal', 'protein', 'fat', 'carb')

admin.site.register(Food, FoodAdmin)
admin.site.register(Target, TargetAdmin)
admin.site.register(Favorite, FavoriteAdmin)