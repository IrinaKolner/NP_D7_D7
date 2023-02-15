from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.http import HttpResponse



class NewsList(ListView):
    model = Post
    ordering = '-time_created'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    # я почему-то решила сделать поиск сразу на странице вывода всех публикаций, пусть оно просто будет здесь, закомментированное
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        # пусть это пока побудет здесь, вдруг пригодится
        # context['next_news'] = "Тут что-то должно быть написано. Зачем оно? Пусть будет!"
        context['news_number'] = Post.objects.all()
        # context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_item.html'
    context_object_name = 'news_item'


class PostSearch(ListView):
    model = Post
    ordering = '-time_created'
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_number'] = Post.objects.all()
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NE'
        return super().form_valid(form)

# было
# class NewsUpdate(UpdateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'news_create.html'
#
#     def form_valid(self, form):
#         post = form.save(commit=False)
#         post.post_type = 'NE'
#         return super().form_valid(form)

class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.post_type == 'AR':
            return HttpResponse('Такой новости не существует.')
        post.save()
        return super().form_valid(form)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.post_type == 'NE':
            return HttpResponse('Такой статьи не существует.')
        post.save()
        return super().form_valid(form)


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news')

