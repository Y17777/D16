
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm, CommentForm
from .models import Bullets, Comment
from .utils import DataMixin


class BulletsHome(DataMixin, ListView):
    model = Bullets
    paginate_by = 4
    template_name = 'board/index.html'
    context_object_name = 'bullets'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Bullets.objects.all().select_related('cat')


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = PostForm
    template_name = 'board/addpage.html'
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        board = form.save(commit=False)
        board.author = self.request.user
        return super().form_valid(form)


class EditPage(LoginRequiredMixin, DataMixin, UpdateView):
    model = Bullets
    fields = ['title', 'content', 'photo', 'cat']
    template_name = 'board/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['b_author'] = Bullets.objects.get(pk=self.kwargs.get('pk')).author
        return context


class DeletePage(PermissionRequiredMixin, DataMixin, DeleteView):
    permission_required = ('board.delete_post',)
    model = Bullets
    template_name = 'board/deletepage.html'
    success_url = reverse_lazy('home')


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'board/post.html'
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post = get_object_or_404(Bullets, pk=self.kwargs['pk'])
        comment.commentAuthor = self.request.user
        comment.commentPost_id = self.kwargs['pk']
        comment.save()
        author = User.objects.get(pk=post.author_id)
        send_mail(
            "Новый отклик на публикацию",
            f"Пользователь {comment.commentAuthor.username} откликнулся на Вашу публикацию {post}.",
            None,
            [author.email],
            fail_silently=False,
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs['pk']
        return context


class ShowPosts(DataMixin, DetailView, CreateComment):
    template_name = 'board/post.html'
    context_object_name = 'show_post'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['show_post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Bullets.objects, pk=self.kwargs[self.pk_url_kwarg])


class ShowUserPosts(LoginRequiredMixin, DataMixin, ListView):
    model = Bullets
    paginate_by = 20
    template_name = 'board/list_mypost.html'
    context_object_name = 'userPost'
    title = f'Bullets.pk | {Bullets.title}'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        return get_object_or_404(Bullets.pk, pk=self.kwargs[self.pk_url_kwarg])


class ShowPostComments(LoginRequiredMixin, DataMixin, ListView):
    model = Comment
    template_name = 'board/list_comments.html'
    context_object_name = 'comments'

    def get_queryset(self, **kwargs):
        return Comment.objects.all().filter(commentPost=self.kwargs['post_pk'])


class DeleteComment(LoginRequiredMixin, DataMixin, DeleteView):
    model = Comment
    template_name = 'board/delete_comment.html'
    success_url = reverse_lazy('home')


def accept_comment(request, **kwargs):
    comment = get_object_or_404(Comment, pk=kwargs['pk'])
    comment.accept_status = 1
    comment.save()
    author = User.objects.get(pk=comment.commentAuthor_id)
    send_mail(
        f"Ваш отклик принят",
        f"Пользователем {comment.commentAuthor.username} Ваш отклик {comment.text} был принят.",
        None,
        [author.email],
        fail_silently=False,
    )
    return HttpResponseRedirect('/accounts/profile')


class BulletsCategory(DataMixin, ListView):
    template_name = 'board/index.html'
    context_object_name = 'bullets'
    allow_empty = False

    def get_queryset(self):
        return Bullets.objects.filter(cat=self.kwargs['pk']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['bullets'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
