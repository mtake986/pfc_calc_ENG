from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Sum, Q
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from base.models import Food, Target
from blog.models import Blog
from django.contrib.auth.models import User
from django.contrib import auth

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta

# Create your views here.
# class CustomLoginView(LoginView):
#   template_name = 'account/login.html'
#   fields = '__all__'
#   # すでにログインしてるのにアクセスするとリダイレクトする
#   redirect_authenticated_user = True

#   def get_success_url(self):
#     return reverse_lazy('today_foods')

# class RegisterPage(FormView):
#   template_name = 'account/register.html'
#   form_class = UserCreationForm
#   redirect_authenticated_user = True
#   success_url = reverse_lazy('today_foods')

#   def form_valid(self, form):
#     user = form.save()
#     if user is not None:
#       login(self.request, user)
#     return super(RegisterPage, self).form_valid(form)

#   def get(self, *args, **kwargs):
#     if self.request.user.is_authenticated:
#       return redirect('today_foods')
#     return super(RegisterPage, self).get(*args, **kwargs)

from django.contrib import messages
def register(request):
  
  if request.method == 'POST':
    # get form values
    username = request.POST['username']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, '※This username is already taken.')
        return redirect('register')
      else:
        # Looks good
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, 'Successfully signed up')
        return redirect('login')
    else:
      messages.error(request, '※Passwords are different. ')
      return redirect('register')
  else:
    return render(request, 'account/register.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)
    if user is not None:
      auth.login(request, user)
      messages.success(request, 'Successfully logged in')
      return redirect('today_foods')
    else:
      messages.error(request, '※Invalid username or password')
      return redirect('login')
  else:
    return render(request, 'account/login.html')

  #   # if this username exists in the database
  #   if User.objects.filter(username=username).exists():
  #     user = auth.authenticate(username=username, password=password)
  #     # Check username and password are correct
  #     if user is not None:
  #       auth.login(request, user)
  #       messages.success(request, 'ログインしました')
  #       return redirect('today_foods')
  #     # if password is wrong 
  #     else:
  #       messages.error(request, '※パスワードが間違っています')
  #       return redirect('login')
    
  #   # if this username doesn't exist in the database
  #   else:
  #     messages.error(request, '※ユーザー名が間違っています')
  #     return redirect('login')
  # else:
  #   return render(request, 'account/login.html')

def logout(request):
  if request.method == 'GET':
    auth.logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('login')

def dashboard(request, pk):
  user = get_object_or_404(User, pk=pk)
  user_blogs = Blog.objects.order_by('-updated').filter(is_public='公開' ,user=request.user)[:5]

  # これは時間分秒ミリ秒まで含んでる
  today = datetime.today()
  yesterday = today - timedelta(days=1)
  two_days_ago = today - timedelta(days=2)
  three_days_ago = today - timedelta(days=3)
  four_days_ago = today - timedelta(days=4)
  five_days_ago = today - timedelta(days=5)
  six_days_ago = today - timedelta(days=6)
  seven_days_ago = today - timedelta(days=7)

  # filter用の月日
  db_yesterday = yesterday.strftime('%Y-%m-%d')
  db_two_days_ago = two_days_ago.strftime('%Y-%m-%d')
  db_three_days_ago = three_days_ago.strftime('%Y-%m-%d')
  db_four_days_ago = four_days_ago.strftime('%Y-%m-%d')
  db_five_days_ago = five_days_ago.strftime('%Y-%m-%d')
  db_six_days_ago = six_days_ago.strftime('%Y-%m-%d')
  db_seven_days_ago = seven_days_ago.strftime('%Y-%m-%d')

  # 表示させる月日
  html_yest = yesterday.strftime('%-m/%-d')
  html_two_days_ago = two_days_ago.strftime('%-m/%-d')
  html_three_days_ago = three_days_ago.strftime('%-m/%-d')
  html_four_days_ago = four_days_ago.strftime('%-m/%-d')
  html_five_days_ago = five_days_ago.strftime('%-m/%-d')
  html_six_days_ago = six_days_ago.strftime('%-m/%-d')
  html_seven_days_ago = seven_days_ago.strftime('%-m/%-d')

  # 昨日のデータを取得
  yesterday_user_foods = Food.objects.all().filter(user=request.user, eaten_date=db_yesterday)
  yest_k = yesterday_user_foods.aggregate(Sum('kcal'))
  yest_p = yesterday_user_foods.aggregate(Sum('protein'))
  yest_f = yesterday_user_foods.aggregate(Sum('fat'))
  yest_c = yesterday_user_foods.aggregate(Sum('carb'))


  # 2日前のデータを取得
  two_days_ago_user_foods = Food.objects.all().filter(user=request.user, eaten_date=db_two_days_ago)
  two_days_ago_k = two_days_ago_user_foods.aggregate(Sum('kcal'))
  two_days_ago_p = two_days_ago_user_foods.aggregate(Sum('protein'))
  two_days_ago_f = two_days_ago_user_foods.aggregate(Sum('fat'))
  two_days_ago_c = two_days_ago_user_foods.aggregate(Sum('carb'))

  # 3日前のデータを取得
  three_days_ago_user_foods = Food.objects.all().filter(user=request.user, eaten_date=db_three_days_ago)
  three_days_ago_k = three_days_ago_user_foods.aggregate(Sum('kcal'))
  three_days_ago_p = three_days_ago_user_foods.aggregate(Sum('protein'))
  three_days_ago_f = three_days_ago_user_foods.aggregate(Sum('fat'))
  three_days_ago_c = three_days_ago_user_foods.aggregate(Sum('carb'))

  # 4日前のデータを取得
  four_days_ago_user_foods = Food.objects.all().filter(user=request.user, eaten_date=db_four_days_ago)
  four_days_ago_k = four_days_ago_user_foods.aggregate(Sum('kcal'))
  four_days_ago_p = four_days_ago_user_foods.aggregate(Sum('protein'))
  four_days_ago_f = four_days_ago_user_foods.aggregate(Sum('fat'))
  four_days_ago_c = four_days_ago_user_foods.aggregate(Sum('carb'))

  # 5日前のデータを取得
  five_days_ago_user_foods = Food.objects.all().filter(user=request.user, eaten_date=db_five_days_ago)
  five_days_ago_k = five_days_ago_user_foods.aggregate(Sum('kcal'))
  five_days_ago_p = five_days_ago_user_foods.aggregate(Sum('protein'))
  five_days_ago_f = five_days_ago_user_foods.aggregate(Sum('fat'))
  five_days_ago_c = five_days_ago_user_foods.aggregate(Sum('carb'))

  # 6日前のデータを取得
  six_days_ago_user_foods = Food.objects.all().filter(user=request.user, eaten_date=db_six_days_ago)
  six_days_ago_k = six_days_ago_user_foods.aggregate(Sum('kcal'))
  six_days_ago_p = six_days_ago_user_foods.aggregate(Sum('protein'))
  six_days_ago_f = six_days_ago_user_foods.aggregate(Sum('fat'))
  six_days_ago_c = six_days_ago_user_foods.aggregate(Sum('carb'))

  # 7日前のデータを取得
  seven_days_ago_user_foods = Food.objects.all().filter(user=request.user, eaten_date=db_seven_days_ago)
  seven_days_ago_k = seven_days_ago_user_foods.aggregate(Sum('kcal'))
  seven_days_ago_p = seven_days_ago_user_foods.aggregate(Sum('protein'))
  seven_days_ago_f = seven_days_ago_user_foods.aggregate(Sum('fat'))
  seven_days_ago_c = seven_days_ago_user_foods.aggregate(Sum('carb'))

  try:
    target = Target.objects.filter(user=request.user).latest('created')
  except Target.DoesNotExist:
    target = None
  context = {
    'user': user,
    'user_blogs': user_blogs,
    # 'yesterday_user_foods': yesterday_user_foods,
    # 'yesterday': yesterday,
    'html_yest': html_yest,
    'html_two_days_ago': html_two_days_ago,
    'html_three_days_ago': html_three_days_ago,
    'html_four_days_ago': html_four_days_ago,
    'html_five_days_ago': html_five_days_ago,
    'html_six_days_ago': html_six_days_ago,
    'html_seven_days_ago': html_seven_days_ago,
    'yest_k': yest_k,
    'yest_p': yest_p,
    'yest_f': yest_f,
    'yest_c': yest_c,
    'two_days_ago_k': two_days_ago_k,
    'two_days_ago_p': two_days_ago_p,
    'two_days_ago_f': two_days_ago_f,
    'two_days_ago_c': two_days_ago_c,
    'three_days_ago_k': three_days_ago_k,
    'three_days_ago_p': three_days_ago_p,
    'three_days_ago_f': three_days_ago_f,
    'three_days_ago_c': three_days_ago_c,
    'four_days_ago_k': four_days_ago_k,
    'four_days_ago_p': four_days_ago_p,
    'four_days_ago_f': four_days_ago_f,
    'four_days_ago_c': four_days_ago_c,
    'five_days_ago_k': five_days_ago_k,
    'five_days_ago_p': five_days_ago_p,
    'five_days_ago_f': five_days_ago_f,
    'five_days_ago_c': five_days_ago_c,
    'six_days_ago_p': six_days_ago_p,
    'six_days_ago_f': six_days_ago_f,
    'six_days_ago_c': six_days_ago_c,
    'six_days_ago_k': six_days_ago_k,
    'seven_days_ago_p': seven_days_ago_p,
    'seven_days_ago_f': seven_days_ago_f,
    'seven_days_ago_c': seven_days_ago_c,
    'seven_days_ago_k': seven_days_ago_k,
    'target':target,
  }
  return render(request, 'account/dashboard.html', context)

def change_username(request, pk):
  user = get_object_or_404(User, pk =pk)
  context = {
    'user': user
  }
  if request.method == 'POST':
    old_username = user.username
    new_username = request.POST['new_username']
    new_username2 = request.POST['new_username2']
    password = request.POST['password']

    user = auth.authenticate(username=old_username, password=password)
    if new_username != new_username2:
      messages.error(request, "※Usernames don't match.")
      return render(request, 'account/change_username.html', context)
    else:
      if user is not None:
        user.username = new_username
        user.save()
        messages.success(request, 'Successfully changed username.')
        return redirect('login')
      else:
        messages.error(request, '※Invalid Password')
        return render(request, 'account/change_username.html', context)
  else:
    return render(request, 'account/change_username.html', context)

# def change_password(request, pk):
#   user = get_object_or_404(User, pk =pk)
#   context = {
#     'user': user
#   }
#   if request.method == 'POST':
#     old_password = request.POST['old_password']
#     new_password = request.POST['new_password']
#     new_password2 = request.POST['new_password2']
#     # Check if passwords match
#     if new_password == new_password2:
#       user.password = new_password
#       user.save()
#       messages.success(request, 'パスワードを変更しました')
#       return redirect('login')
#     else:
#       messages.error(request, '※パスワードが一致していません')
#       return render(request, 'account/change_password.html', context)
#   else:
#     return render(request, 'account/change_password.html', context)