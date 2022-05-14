from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
BLOG_IS_PUBLIC = (('公開','公開'),('非公開','非公開'))
class Blog(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='ユーザー')
  title = models.CharField(max_length=200, verbose_name='タイトル')
  content_1 = models.TextField(verbose_name='コンテンツ1')
  content_2 = models.TextField(verbose_name='コンテンツ2', null=True, blank=True)
  content_3 = models.TextField(verbose_name='コンテンツ3', null=True, blank=True)
  link_1 = models.URLField(verbose_name='参考文献リンク1', max_length=300, null=True, blank=True)
  link_2 = models.URLField(verbose_name='参考文献リンク2', max_length=300, null=True, blank=True)
  # category = models.CharField(max_length=200, choices=CATEGORY)
  is_public = models.CharField(max_length=200, choices=BLOG_IS_PUBLIC, verbose_name='公開設定', default='公開')
  created = models.DateTimeField(auto_now_add=True, verbose_name='作成日')
  updated = models.DateTimeField(auto_now=True, verbose_name='更新日')
  tags = TaggableManager(blank=True, help_text="※複数加える場合は、ではなく, で区切ってください")
  def __str__(self):
    return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', max_length=200)
    text = models.TextField(verbose_name='コメント')
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    # approved_comment = models.BooleanField(default=False)

    # def approve(self):
    #     self.approved_comment = True
    #     self.save()

    def __str__(self):
        return self.text