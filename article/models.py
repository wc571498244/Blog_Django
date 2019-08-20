from django.db import models
from mdeditor.fields import MDTextField

from user.models import UserProfile


# 标签模型
class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tag"
        verbose_name = "标签表"
        verbose_name_plural = verbose_name


# 文章模型
class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name="文章标题")
    desc = models.CharField(max_length=100, verbose_name="简介")
    date = models.DateTimeField(auto_now=True, verbose_name="发表时间")
    content = MDTextField(verbose_name="内容")  # MDTextField   markdown 字段
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    love_num = models.IntegerField(default=0, verbose_name="收藏量")
    img = models.ImageField(upload_to="uploads/article/%Y/%m/%d", verbose_name="文章图片")

    tags = models.ManyToManyField(to=Tag)
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "article"
        verbose_name = "文章表"
        verbose_name_plural = verbose_name


class Comments(models.Model):
    content = models.TextField(verbose_name="评论内容")
    date = models.DateTimeField(auto_now=True, verbose_name="评论日期")
    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name="评论用户")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="文章")

    class Meta:
        db_table = 'comments'
        verbose_name = "评论表"
        verbose_name_plural = verbose_name
