from django.urls import path
from .views import FoodCreate, FoodUpdate, FoodDelete, FoodList, TargetCreate

from . import views

urlpatterns = [
    path('', views.today_foods, name='today_foods'),
    path('all_foods', FoodList.as_view(), name='all_foods'),
    path('all_foods/search/', views.food_search, name='food_search'),
    # path('change_number_of_foods', views.change_number_of_foods, name='change_number_of_foods'),
    path('favorite', views.favorite, name='favorite'),
    path('favorite/register', views.favorite_register, name='favorite_register'),
    path('favorite/delete/<int:pk>', views.favorite_delete, name='favorite_delete'),
    path('favorite/update/<int:pk>', views.favorite_update, name='favorite_update'),
    path('favorite/add_to_today_foods/<int:pk>',views.add_to_today_foods, name='add_to_today_foods'),
    path('target', TargetCreate.as_view(), name='target'),
    # path('', FoodList.as_view(), name='foods'),
    path('create/', FoodCreate.as_view(), name='food_create'),
    path('update/<int:pk>', FoodUpdate.as_view(), name='food_update'),
    path('delete/<int:pk>', FoodDelete.as_view(), name='food_delete'),

]
