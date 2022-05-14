from django import forms
from .models import Food, Favorite
class FoodForm(forms.ModelForm):
  class Meta:
    model = Food
    fields = ('category', 'name', 'kcal', 'protein', 'fat', 'carb', 'eaten_date',)

class FavoriteForm(forms.ModelForm):
  class Meta:
    model = Favorite
    fields = ('category', 'name', 'kcal', 'protein', 'fat', 'carb',)