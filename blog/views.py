from django.shortcuts import render, get_object_or_404
from account.models import User
from account.mixins import SuperUserAccessMixin
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import Article, Category

# Create your views here.
# def home(request, page=1):
#     article_list = Article.objects.published()
#     paginator = Paginator(article_list, 6)
#     articles = paginator.get_page(page)
#     context = {
#         'articles': articles,
#     }
#     return render(request, 'blog/home.html', context)
class ArticleList(ListView):
    # model = Article
    # template_name = 'blog/home.html'
    # context_object_name = "articles"
    queryset = Article.objects.published()
    paginate_by = 6


# def detail(request, slug):
#     context = {
#         'article': get_object_or_404(Article.objects.published(), slug=slug)
#     }
#     return render(request, 'blog/detail.html', context)
class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(), slug=slug)


# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     article_list = category.articles.published()
#     paginator = Paginator(article_list, 3)
#     articles = paginator.get_page(page)
#     context = {
#         'category': category,
#         'articles': articles
#     }
#     return render(request, 'blog/category.html', context)
class CategoryList(ListView):
    paginate_by = 3
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()

    # for editing context and add category to context and send it
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    paginate_by = 3
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()

    # for editing context and add author to context and send it
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context


class ArticlePreview(SuperUserAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)