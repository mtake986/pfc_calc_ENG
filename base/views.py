from .choices import category_choices
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# function-based view 用のアクセス制限
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum, Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Food, Target, Favorite
from blog.models import Blog
from datetime import datetime, date, timedelta
from .forms import FoodForm, FavoriteForm


@login_required
def today_foods(request):
    today = datetime.today()
    # foods = Food.objects.filter(eaten_date=today)
    user_foods = Food.objects.order_by(
        '-category').filter(user=request.user, eaten_date=today)
    try:
        target = Target.objects.filter(user=request.user).latest('created')
    except Target.DoesNotExist:
        target = None
    user_breakfast_list = user_foods.filter(category='Breakfast')
    user_lunch_list = user_foods.filter(category='Lunch')
    user_snack_list = user_foods.filter(category='Snack')
    user_dinner_list = user_foods.filter(category='Dinner')
    # これでも合計カロリーは出る
    # kcal = foods.aggregate(Sum('kcal'))
    # protein = foods.aggregate(Sum('protein'))

    # total_kcal
    kcal_list = [food['kcal'] for food in user_foods.values('kcal')]
    ttl_kcal = sum(kcal_list)
    # total_protein
    protein_list = [food['protein'] for food in user_foods.values('protein')]
    ttl_protein = sum(protein_list)
    # total_fat
    fat_list = [food['fat'] for food in user_foods.values('fat')]
    ttl_fat = sum(fat_list)
    # total_carb
    carb_list = [food['carb'] for food in user_foods.values('carb')]
    ttl_carb = sum(carb_list)

    context = {
        'ttl_kcal': ttl_kcal,
        'ttl_protein': ttl_protein,
        'ttl_fat': ttl_fat,
        'ttl_carb': ttl_carb,
        'user_foods': user_foods,
        'user_breakfast_list': user_breakfast_list,
        'user_lunch_list': user_lunch_list,
        'user_dinner_list': user_dinner_list,
        'user_snack_list': user_snack_list,
        'target': target,
    }
    return render(request, 'base/today_foods.html', context)


class FoodList(LoginRequiredMixin, ListView):
    model = Food
    template_name = 'base/all_foods.html'
    context_object_name = 'foods'
    ordering = ('-created')
    paginate_by = 100
    # def get(self, request, *args, **kwargs):
    #   paginate_by = request.GET.get('number-of-foods')
    #   return paginate_by
    # BlogListと違って、自分の食べ物を表示

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = category_choices
        return context
    # def get_context_data(self, **kwargs):
    #   context = super().get_context_data(**kwargs)
    #   context内の名前で左の値がhtml上で使えるようになる
    #   context['color'] = 'red'
    #   context['foods'] = Food.objects.order_by('-created').filter(user=self.request.user)
    #   return context
    #   search_input = self.request.GET.get('search-area') or ''
    #   if search_input:
    #     context['foods'] = context['foods'].filter(Q(name__icontains=search_input)|Q(category__icontains=search_input))
    #   context['search_input'] = search_input
    #   return context


@login_required
def food_search(request):
    foods = Food.objects.order_by('-created').filter(user=request.user)
    # paginator = Paginator(foods, 20)
    # page = request.GET.get('page')
    # paged_foods = paginator.get_page(page)

    # both
    if 'food1' in request.GET and 'food2' in request.GET:
        food1 = request.GET['food1']
        food2 = request.GET['food2']
        if food1 and food2:
            foods = foods.filter(Q(name__icontains=food1)
                                 | Q(name__icontains=food2))
        elif food1:
            foods = foods.filter(Q(name__icontains=food1))
        elif food2:
            foods = foods.filter(Q(name__icontains=food2))
    # date
    if 'date' in request.GET:
        date = request.GET['date']
        if date:
            foods = foods.filter(user=request.user, eaten_date__icontains=date)

    # category
    if 'category' in request.GET:
        category = request.GET['category']
        if category != '全て':
            foods = foods.filter(user=request.user, category__iexact=category)
        # else:
        #   foods = foods.filter(user=request.user)

    context = {
        'foods':  foods,
        'category_choices':  category_choices,
        # 'paged_foods': paged_foods,
        'values': request.GET,
    }

    return render(request, 'base/all_foods.html', context)

# def change_number_of_foods(request):
#   pass


class TargetCreate(LoginRequiredMixin, CreateView):
    template_name = 'base/target.html'
    model = Target
    fields = '__all__'
    success_url = reverse_lazy('today_foods')
    context_object_name = 'targets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['target'] = Target.objects.filter(
                user=self.request.user).latest('created')
        except Target.DoesNotExist:
            context['target'] = None
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TargetCreate, self).form_valid(form)


def favorite(request):
    favorites = Favorite.objects.all().filter(user=request.user)
    br_favs = favorites.filter(category='Breakfast')
    lu_favs = favorites.filter(category='Lunch')
    di_favs = favorites.filter(category='Dinner')
    sn_favs = favorites.filter(category='Snack')
    number_of_favorites = favorites.count()

    context = {
        'favorites': favorites,
        'br_favs': br_favs,
        'lu_favs': lu_favs,
        'di_favs': di_favs,
        'sn_favs': sn_favs,
        'number_of_favorites': number_of_favorites,
    }
    return render(request, 'base/favorite.html', context)

def favorite_register(request):
    if request.method == 'GET':
        form = FavoriteForm()
    elif request.method == 'POST':
        form = FavoriteForm(request.POST)
        if form.is_valid():
            favorite = form.save(commit=False)
            favorite.user = request.user
            favorite.save()
            form = FavoriteForm()
            return redirect('favorite')
    context = {
        'form': form, 
    }
    return render(request, 'base/favorite_register.html', context)

def favorite_delete(request, pk):
    favorite = get_object_or_404(Favorite, pk=pk)
    if request.method == 'POST':
        favorite.delete()
        return redirect('favorite')
    context = {
        'favorite': favorite,
    }
    return render(request, 'base/favorite_delete.html', context)


def favorite_update(request, pk):
    favorite = get_object_or_404(Favorite, pk=pk)
    if request.method == 'POST':
        form = FavoriteForm(request.POST, instance=favorite)
        if form.is_valid():
            form.save()
            return redirect('favorite')
    else:
        form = FavoriteForm(instance=favorite)
    context = {
        'form': form,
        'favorite': favorite,
    }
    return render(request, 'base/favorite_update.html', context)

# @require_POST
# def add_favorite_to_today_foods(request, pk):
#   favorite = get_object_or_404(Favorite, pk=pk)
#   form = FoodForm(instance=favorite)
#   if form.is_valid():
#     form.save()
#     return redirect('today_foods')
#   context = {
#     'favorite': favorite,
#     'form': form,
#   }
#   print(context)
#   return render(request, 'base/create.html', context)


def add_to_today_foods(request, pk):
    favorite = get_object_or_404(Favorite, pk=pk)
    food = Food()

    food.user = favorite.user
    food.name = favorite.name
    food.category = favorite.category
    food.kcal = favorite.kcal
    food.protein = favorite.protein
    food.fat = favorite.fat
    food.carb = favorite.carb
    food.eaten_date = datetime.today()
    food.save()

    return redirect('today_foods')


class FoodCreate(LoginRequiredMixin, CreateView):
    template_name = 'base/create.html'
    model = Food
    fields = ['category', 'name', 'kcal',
              'protein', 'fat', 'carb', 'eaten_date']
    success_url = reverse_lazy('today_foods')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # form.instance.eaten_date = datetime.now().strftime('%Y-%m-%d')
        return super(FoodCreate, self).form_valid(form)


class FoodUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'base/update.html'
    model = Food
    fields = ['category', 'name', 'kcal',
              'protein', 'fat', 'carb', 'eaten_date']
    success_url = reverse_lazy('today_foods')


class FoodDelete(LoginRequiredMixin, DeleteView):
    template_name = 'base/delete.html'
    model = Food
    context_object_name = 'food'
    success_url = reverse_lazy('today_foods')

