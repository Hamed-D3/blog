from django.db import models
from account.models import User
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from extensions.utils import jalali_converter


# my managers
class ArticleManager(models.Manager):
    
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    
    def active(self):
        return self.filter(status=True)


# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True,
    on_delete=models.SET_NULL, related_name='children', verbose_name="زیردسته")
    title = models.CharField(max_length=200, verbose_name="عنوان دسته‌بندی")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس دسته‌بندی")
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
    position = models.IntegerField(verbose_name="موقعیت")

    class Meta:
        # for single name
        verbose_name = "دسته‌بندی"
        # for sumation name
        verbose_name_plural = "دسته‌بندی‌ها"

        # default ordering push on model
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش‌نویس'),       # draft
        ('p', 'منتشر شده'),     # publish
        ('i', "در حال بررسی"),  # investigation
        ('b', "برگشت داده شده") # back
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles',
                                verbose_name="نویسنده")
    title = models.CharField(max_length=200, verbose_name="عنوان مقاله")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس مقاله")
    category = models.ManyToManyField(Category, verbose_name="دسته‌بندی", related_name="articles")
    description = models.TextField(verbose_name="محتوا")
    thumbnail = models.ImageField(upload_to='images', verbose_name="تصویر مقاله")
    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    is_special = models.BooleanField(default=False, verbose_name="مقاله ویژه")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status  = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")

    class Meta:
        # for single name
        verbose_name = "مقاله"
        # for sumation name
        verbose_name_plural = "مقالات"
        ordering = ['-publish']

    def __str__(self):
        return self.title

    # return jalali of publish time
    def jpublish(self):
        return jalali_converter(self.publish)

    # for name in admin panel
    jpublish.short_description = "زمان انتشار"


    def thumbnail_tag(self):
        return format_html(f"<img src='{self.thumbnail.url}' style='width:100px;height:60px;border-radius:5px;'>")
    thumbnail_tag.short_description = "عکس شاخص"

    def category_to_str(self):
        return '، '.join([category.title for category in self.category.active()])
    category_to_str.short_description = "دسته‌بندی"

    def get_absolute_url(self):
        return reverse('account:home')

    # set new manager for article
    objects = ArticleManager()