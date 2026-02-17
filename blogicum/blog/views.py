from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count  # Добавьте этот импорт

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post


def index(request):
    # Добавляем аннотацию с количеством комментариев
    post_list = Post.objects.filter(
        is_published=True,
        category__is_published=True  # Добавьте эту фильтрацию
    ).annotate(
        comment_count=Count('comments')  # Считаем комментарии
    ).order_by('-pub_date')

    paginator = Paginator(post_list, 10)  # 10 постов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    # Добавляем аннотацию и для детальной страницы
    post = get_object_or_404(
        Post.objects.annotate(
            comment_count=Count('comments')
        ), 
        id=post_id, 
        is_published=True
    )
    comments = Comment.objects.filter(post=post).order_by('created_at')
    form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'comments_count': comments.count(),
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    post_list = Post.objects.filter(
        category=category, 
        is_published=True
    ).annotate(
        comment_count=Count('comments')  # Добавляем аннотацию
    ).order_by('-pub_date')

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category.html', {'category': category, 'page_obj': page_obj})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).annotate(
        comment_count=Count('comments')  # Добавляем аннотацию
    ).order_by('-pub_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/profile.html', {
        'profile': user,
        'page_obj': page_obj
    })


@login_required
def profile_edit(request):
    # Ваша существующая функция
    pass


@login_required
def post_create(request):
    """Создание нового поста."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()

    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    """Редактирование поста."""
    post = get_object_or_404(Post, id=post_id)

    # Проверка прав доступа
    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post.id)

    # Обработка POST запроса
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        # GET запрос - показываем форму с данными поста
        form = PostForm(instance=post)

    # Используем тот же шаблон, что и для создания поста
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    return render(request, 'blog/delete_post.html', {'post': post})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
        return redirect('blog:post_detail', post_id=post.id)
    return redirect('blog:post_detail', post_id=post.id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = CommentForm(instance=comment)

    context = {'form': form, 'post': comment.post, 'comment': comment}
    return render(request, 'blog/edit_comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/delete_comment.html', {'comment': comment, 'post': comment.post})
