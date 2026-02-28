from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post, Comment, UserSurvey
from .forms import UserRegisterForm, CommentForm, UserSurveyForm

# ... (other views remain)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_superuser or self.request.user == post.author

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if request.user.is_superuser or request.user == comment.author or request.user == comment.post.author:
        comment.delete()
        messages.success(request, 'Комментарий удален!')
    else:
        messages.error(request, 'У вас нет прав для удаления этого комментария.')
    return redirect('post_detail', pk=post_pk)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Latest 5 posts for the slider
        context['slider_posts'] = Post.objects.all()[:5]
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_date')
        context['comment_form'] = CommentForm()
        return context

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Ваш комментарий добавлен!')
    return redirect('post_detail', pk=pk)

@login_required
def survey(request):
    try:
        user_survey = request.user.survey
    except UserSurvey.DoesNotExist:
        user_survey = None

    if request.method == 'POST':
        form = UserSurveyForm(request.POST, instance=user_survey)
        if form.is_valid():
            survey_instance = form.save(commit=False)
            survey_instance.user = request.user
            survey_instance.save()
            messages.success(request, 'Анкета успешно сохранена!')
            return redirect('home')
    else:
        form = UserSurveyForm(instance=user_survey)
    return render(request, 'blog/survey.html', {'form': form})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'video']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'video']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})
