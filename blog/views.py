from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Blog, Comment
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, date, timedelta
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

from .forms import CommentForm
from base.choices import category_choices
# Create your views here.


@login_required
def index(request):
    # Add 'NEW!!' if a blog was created yesterday or today
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    today_created_blogs = Blog.objects.all().filter(
        is_public='公開', created__date=today)
    yes_created_blogs = Blog.objects.all().filter(
        is_public='公開', created__date=yesterday)
    today_updated_blogs = Blog.objects.all().filter(
        is_public='公開', updated__date=today)
    yes_updated_blogs = Blog.objects.all().filter(
        is_public='公開', updated__date=yesterday)

    count = Blog.objects.order_by(
        '-updated').filter(is_public='公開', created__date=today).count()

    blogs = Blog.objects.order_by('-updated').filter(is_public='公開')[:10]

    # print(f'today -> {today}')
    # print(f'yesterday -> {yesterday}')
    # print(f'today_blogs -> {today_blogs}')
    # print(f'yesterday_blogs -> {yesterday_blogs}')
    # print(f'blogs -> {blogs}')
    # print(f'today blogs -> {count}')

    context = {
        'blogs': blogs,
        'today_created_blogs': today_created_blogs,
        'yes_created_blogs': yes_created_blogs,
        'today_updated_blogs': today_updated_blogs,
        'yes_updated_blogs': yes_updated_blogs,
        'count': count,
    }
    return render(request, 'blog/latest_blogs.html', context)


class BlogList(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blog/all_blogs.html'
    context_object_name = 'blogs'
    ordering = ('-updated')
    paginate_by = 10

    # FoodListと違って、全ユーザーの記事を表示
    def get_queryset(self):
        queryset = super().get_queryset().filter(is_public='公開')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.today()
        # context['blogs'] = Blog.objects.order_by('-created').filter(is_public='公開')
        yesterday = today - timedelta(days=1)
        context['today_created_blogs'] = Blog.objects.all().filter(
            is_public='公開', created__date=today)
        context['yes_created_blogs'] = Blog.objects.all().filter(
            is_public='公開', created__date=yesterday)
        context['today_updated_blogs'] = Blog.objects.all().filter(
            is_public='公開', updated__date=today)
        context['yes_updated_blogs'] = Blog.objects.all().filter(
            is_public='公開', updated__date=yesterday)
        context['category_choices'] = category_choices
        return context
    (category_choices)


@login_required
def all_blogs_search(request):
    # Add 'NEW!!' if a blog was created yesterday or today
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    today_created_blogs = Blog.objects.all().filter(
        is_public='公開', created__date=today)
    yes_created_blogs = Blog.objects.all().filter(
        is_public='公開', created__date=yesterday)
    today_updated_blogs = Blog.objects.all().filter(
        is_public='公開', updated__date=today)
    yes_updated_blogs = Blog.objects.all().filter(
        is_public='公開', updated__date=yesterday)

    blogs = Blog.objects.order_by('-updated').filter(is_public='公開')

    # paginator = Paginator(queryset_list, 10)
    # page = request.GET.get('page')
    # paged_blogs = paginator.get_page(page)

    if 'keyword1' in request.GET and 'keyword2' in request.GET and 'keyword3' in request.GET:
        keyword1 = request.GET['keyword1']
        keyword2 = request.GET['keyword2']
        keyword3 = request.GET['keyword3']
        if keyword1 and keyword2 and keyword3:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword1) |
                Q(content_1__icontains=keyword1) |
                Q(content_2__icontains=keyword1) |
                Q(content_3__icontains=keyword1) |
                Q(user__username__icontains=keyword1) |
                Q(tags__name__in=[keyword1]) |
                # 2
                Q(title__icontains=keyword2) |
                Q(content_1__icontains=keyword2) |
                Q(content_2__icontains=keyword2) |
                Q(content_3__icontains=keyword2) |
                Q(user__username__icontains=keyword2) |
                Q(tags__name__in=[keyword2]) |
                # 3
                Q(title__icontains=keyword3) |
                Q(content_1__icontains=keyword3) |
                Q(content_2__icontains=keyword3) |
                Q(content_3__icontains=keyword3) |
                Q(user__username__icontains=keyword3) |
                Q(tags__name__in=[keyword3])
            )
        elif keyword1 and keyword2:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword1) |
                Q(content_1__icontains=keyword1) |
                Q(content_2__icontains=keyword1) |
                Q(content_3__icontains=keyword1) |
                Q(user__username__icontains=keyword1) |
                Q(tags__name__in=[keyword1]) |
                # 2
                Q(title__icontains=keyword2) |
                Q(content_1__icontains=keyword2) |
                Q(content_2__icontains=keyword2) |
                Q(content_3__icontains=keyword2) |
                Q(user__username__icontains=keyword2) |
                Q(tags__name__in=[keyword2])
            )
        elif keyword1 and keyword3:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword1) |
                Q(content_1__icontains=keyword1) |
                Q(content_2__icontains=keyword1) |
                Q(content_3__icontains=keyword1) |
                Q(user__username__icontains=keyword1) |
                Q(tags__name__in=[keyword1]) |
                # 2
                Q(title__icontains=keyword3) |
                Q(content_1__icontains=keyword3) |
                Q(content_2__icontains=keyword3) |
                Q(content_3__icontains=keyword3) |
                Q(user__username__icontains=keyword3) |
                Q(tags__name__in=[keyword3])
            )
        elif keyword2 and keyword3:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword2) |
                Q(content_1__icontains=keyword2) |
                Q(content_2__icontains=keyword2) |
                Q(content_3__icontains=keyword2) |
                Q(user__username__icontains=keyword2) |
                Q(tags__name__in=[keyword2]) |
                # 2
                Q(title__icontains=keyword3) |
                Q(content_1__icontains=keyword3) |
                Q(content_2__icontains=keyword3) |
                Q(content_3__icontains=keyword3) |
                Q(user__username__icontains=keyword3) |
                Q(tags__name__in=[keyword3])
            )
        elif keyword1:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword1) |
                Q(content_1__icontains=keyword1) |
                Q(content_2__icontains=keyword1) |
                Q(content_3__icontains=keyword1) |
                Q(user__username__icontains=keyword1) |
                Q(tags__name__in=[keyword1])
            )
        elif keyword2:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword2) |
                Q(content_1__icontains=keyword2) |
                Q(content_2__icontains=keyword2) |
                Q(content_3__icontains=keyword2) |
                Q(user__username__icontains=keyword2) |
                Q(tags__name__in=[keyword2])
            )
        elif keyword3:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword3) |
                Q(content_1__icontains=keyword3) |
                Q(content_2__icontains=keyword3) |
                Q(content_3__icontains=keyword3) |
                Q(user__username__icontains=keyword3) |
                Q(tags__name__in=[keyword3])
            )

    context = {
        'blogs': blogs,
        # 'paged_blogs': paged_blogs,
        'today_created_blogs': today_created_blogs,
        'yes_created_blogs': yes_created_blogs,
        'today_updated_blogs': today_updated_blogs,
        'yes_updated_blogs': yes_updated_blogs,
        'values': request.GET
    }

    return render(request, 'blog/all_blogs.html', context)


@login_required
def my_blogs(request):
    # Add 'NEW!!' if a blog was created yesterday or today
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    today_created_blogs = Blog.objects.all().filter(
        is_public='公開', created__date=today)
    yes_created_blogs = Blog.objects.all().filter(
        is_public='公開', created__date=yesterday)
    today_updated_blogs = Blog.objects.all().filter(
        is_public='公開', updated__date=today)
    yes_updated_blogs = Blog.objects.all().filter(
        is_public='公開', updated__date=yesterday)

    blogs = Blog.objects.order_by(
        '-updated').filter(user=request.user, is_public='公開')

    context = {
        'blogs': blogs,
        'today_created_blogs': today_created_blogs,
        'yes_created_blogs': yes_created_blogs,
        'today_updated_blogs': today_updated_blogs,
        'yes_updated_blogs': yes_updated_blogs,
        # 'count': count,
    }
    return render(request, 'blog/my_blogs.html', context)


@login_required
def my_blogs_search(request):
    # Add 'NEW!!' if a blog was created yesterday or today
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    today_created_blogs = Blog.objects.all().filter(
        is_public='公開', created__date=today)
    yes_created_blogs = Blog.objects.all().filter(
        is_public='公開', created__date=yesterday)
    today_updated_blogs = Blog.objects.all().filter(
        is_public='公開', updated__date=today)
    yes_updated_blogs = Blog.objects.all().filter(
        is_public='公開', updated__date=yesterday)

    blogs = Blog.objects.order_by(
        '-updated').filter(user=request.user, is_public='公開')

    # paginator = Paginator(queryset_list, 10)
    # page = request.GET.get('page')
    # paged_blogs = paginator.get_page(page)

    if 'keyword1' in request.GET and 'keyword2' in request.GET and 'keyword3' in request.GET:
        keyword1 = request.GET['keyword1']
        keyword2 = request.GET['keyword2']
        keyword3 = request.GET['keyword3']
        if keyword1 and keyword2 and keyword3:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword1) |
                Q(content_1__icontains=keyword1) |
                Q(content_2__icontains=keyword1) |
                Q(content_3__icontains=keyword1) |
                Q(user__username__icontains=keyword1) |
                Q(tags__name__in=[keyword1]) |
                # 2
                Q(title__icontains=keyword2) |
                Q(content_1__icontains=keyword2) |
                Q(content_2__icontains=keyword2) |
                Q(content_3__icontains=keyword2) |
                Q(user__username__icontains=keyword2) |
                Q(tags__name__in=[keyword2]) |
                # 3
                Q(title__icontains=keyword3) |
                Q(content_1__icontains=keyword3) |
                Q(content_2__icontains=keyword3) |
                Q(content_3__icontains=keyword3) |
                Q(user__username__icontains=keyword3) |
                Q(tags__name__in=[keyword3])
            )
        elif keyword1 and keyword2:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword1) |
                Q(content_1__icontains=keyword1) |
                Q(content_2__icontains=keyword1) |
                Q(content_3__icontains=keyword1) |
                Q(user__username__icontains=keyword1) |
                Q(tags__name__in=[keyword1]) |
                # 2
                Q(title__icontains=keyword2) |
                Q(content_1__icontains=keyword2) |
                Q(content_2__icontains=keyword2) |
                Q(content_3__icontains=keyword2) |
                Q(user__username__icontains=keyword2) |
                Q(tags__name__in=[keyword2])
            )
        elif keyword1 and keyword3:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword1) |
                Q(content_1__icontains=keyword1) |
                Q(content_2__icontains=keyword1) |
                Q(content_3__icontains=keyword1) |
                Q(user__username__icontains=keyword1) |
                Q(tags__name__in=[keyword1]) |
                # 2
                Q(title__icontains=keyword3) |
                Q(content_1__icontains=keyword3) |
                Q(content_2__icontains=keyword3) |
                Q(content_3__icontains=keyword3) |
                Q(user__username__icontains=keyword3) |
                Q(tags__name__in=[keyword3])
            )
        elif keyword2 and keyword3:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword2) |
                Q(content_1__icontains=keyword2) |
                Q(content_2__icontains=keyword2) |
                Q(content_3__icontains=keyword2) |
                Q(user__username__icontains=keyword2) |
                Q(tags__name__in=[keyword2]) |
                # 2
                Q(title__icontains=keyword3) |
                Q(content_1__icontains=keyword3) |
                Q(content_2__icontains=keyword3) |
                Q(content_3__icontains=keyword3) |
                Q(user__username__icontains=keyword3) |
                Q(tags__name__in=[keyword3])
            )
        elif keyword1:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword1) |
                Q(content_1__icontains=keyword1) |
                Q(content_2__icontains=keyword1) |
                Q(content_3__icontains=keyword1) |
                Q(user__username__icontains=keyword1) |
                Q(tags__name__in=[keyword1])
            )
        elif keyword2:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword2) |
                Q(content_1__icontains=keyword2) |
                Q(content_2__icontains=keyword2) |
                Q(content_3__icontains=keyword2) |
                Q(user__username__icontains=keyword2) |
                Q(tags__name__in=[keyword2])
            )
        elif keyword3:
            blogs = blogs.filter(
                # 1
                Q(title__icontains=keyword3) |
                Q(content_1__icontains=keyword3) |
                Q(content_2__icontains=keyword3) |
                Q(content_3__icontains=keyword3) |
                Q(user__username__icontains=keyword3) |
                Q(tags__name__in=[keyword3])
            )

    context = {
        'blogs': blogs,
        # 'paged_blogs': paged_blogs,
        'today_created_blogs': today_created_blogs,
        'yes_created_blogs': yes_created_blogs,
        'today_updated_blogs': today_updated_blogs,
        'yes_updated_blogs': yes_updated_blogs,
        'values': request.GET
    }

    return render(request, 'blog/my_blogs.html', context)


@login_required
def drafts(request):
    user_drafts = Blog.objects.order_by(
        '-created').filter(user=request.user, is_public='非公開')
    context = {
        # 'user': user,
        'user_drafts': user_drafts,
    }
    return render(request, 'blog/drafts.html', context)


@login_required
def blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = Comment.objects.order_by('-created').filter(blog=blog.id)
    number_of_comments = comments.count()
    if request.method == 'GET':
        form = CommentForm()
    elif request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            form = CommentForm()
            return redirect('blog', pk=blog.id)

    if blog.link_1 is not None or blog.link_2 is not None:
        link_1 = blog.link_1
        link_2 = blog.link_2
        context = {
            'blog': blog,
            'link_1': link_1,
            'link_2': link_2,
            'form': form,
            'comments': comments,
            'number_of_comments': number_of_comments,
        }
    else:
        context = {
            'blog': blog,
            'form': form,
            'comments': comments,
            'number_of_comments': number_of_comments,

        }
    return render(request, 'blog/blog.html', context)


# @login_required
# def add_comment(request, pk):
#   blog = get_object_or_404(Blog, pk=pk)
#   if request.method == 'GET':
#     form = CommentForm()
#   if request.method == 'POST':
#     form = CommentForm(request.POST)
#     if form.is_valid():
#       comment = form.save(commit=False)
#       comment.blog = blog
#       comment.user = request.user
#       comment.save()
#       return redirect('blog', pk=blog.pk)

#   context = {
#     'form': form,
#   }
#   return render(request, 'blog/blog.html', context)

class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog/create.html'
    fields = ['title', 'content_1', 'content_2',
              'content_3', 'link_1', 'link_2', 'tags', 'is_public']
    success_url = reverse_lazy('latest_blogs')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BlogCreate, self).form_valid(form)
        

from django.urls import reverse

class BlogUpdate(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog/update.html'
    fields = ['title', 'content_1', 'content_2',
              'content_3', 'link_1', 'link_2', 'tags', 'is_public']
    # success_url = reverse_lazy('latest_blogs')
    def get_success_url(self):
        return reverse('blog', kwargs={'pk': self.kwargs['pk']})


class BlogDelete(LoginRequiredMixin, DeleteView):
    template_name = 'blog/delete.html'
    model = Blog
    context_object_name = 'blog'
    success_url = reverse_lazy('latest_blogs')


@login_required
def comment_update(request, blog_id, comment_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog', pk=blog_id)
    else:
        form = CommentForm(instance=comment)
    context = {
        'blog': blog,
        'comment': comment,
        'form': form,
    }
    return render(request, 'blog/comment_update.html', context)


@login_required
def comment_delete(request, blog_id, comment_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog', pk=blog_id)

    context = {
        'blog': blog,
        'comment': comment,
    }
    return render(request, 'blog/comment_delete.html', context)


@login_required
def tag_redirect(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    tags = blog.tags.all
    return redirect('all_blogs_search')