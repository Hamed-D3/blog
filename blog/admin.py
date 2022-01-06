from django.contrib import admin
from .models import Article, Category

# Register your models here.
def make_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = "منتشر شد."
    else:
        message_bit = "منتشر شدند."
    modeladmin.message_user(request, f"{rows_updated} مقاله {message_bit}")
make_published.short_description = "انتشار مقالات انتخاب شده"

def make_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status='d')
    if rows_updated == 1:
        message_bit = "پیش‌نویس شد."
    else:
        message_bit = "پیش‌نویس شدند."
    modeladmin.message_user(request, f"{rows_updated} مقاله {message_bit}")
make_draft.short_description = "پیش‌نویس شدن مقالات انتخاب شده"

def make_active(modeladmin, request, queryset):
    rows_updated = queryset.update(status=True)
    if rows_updated == 1:
        message_bit = "نمایش داده شد."
    else:
        message_bit = "نمایش داده شدند."
    modeladmin.message_user(request, f"{rows_updated} دسته‌بندی {message_bit}")
make_active.short_description = "نمایش دسته‌بندی انتخاب شده"

def make_disable(modeladmin, request, queryset):
    rows_updated = queryset.update(status=False)
    modeladmin.message_user(request, f"{rows_updated} دسته‌بندی غیر فعال شد.")
make_disable.short_description = "عدم نمایش دسته‌بندی انتخاب شده"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['position', 'title', 'slug', 'parent', 'status']
    list_filter = ['status']
    search_fields = ['title', 'slug']
    actions = [make_active, make_disable]

    # create slug field from title of article
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'thumbnail_tag', 'slug', 'author', 'jpublish', 'status', 'category_to_str']
    list_filter = ['author', 'publish', 'status']
    search_fields = ['title', 'description']
    ordering = ['status', 'publish']
    actions = [make_published, make_draft]

    # create slug field from title of article
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Article, ArticleAdmin)