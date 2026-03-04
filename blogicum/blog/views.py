from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Category, Post, Comment
from .forms import PostForm, CommentForm

POSTS_PER_PAGE_INDEX = 10
POSTS_PER_PAGE_CATEGORY = 10


def get_base_post_queryset():
    return Post.objects.select_related(
        'category', 'author', 'location'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )


def index(request):
    post_list = get_base_post_queryset()
    paginator = Paginator(post_list, POSTS_PER_PAGE_INDEX)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'user': request.user,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    # Пробуем найти пост без фильтрации по публикации
    post = get_object_or_404(Post, id=post_id)

    # Проверяем доступность поста
    is_published = (
        post.is_published
        and post.pub_date <= timezone.now()
        and post.category.is_published
    )

    # Если пост не опубликован и пользователь не автор - 404
    if not is_published and (
        not request.user.is_authenticated
        or post.author != request.user
    ):
        raise Http404

    comments = post.comments.all()
    context = {
        'user': request.user,
        'post': post,
        'comments': comments,
        'comment_form': CommentForm(),
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_base_post_queryset().filter(category=category)
    paginator = Paginator(post_list, POSTS_PER_PAGE_CATEGORY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category, 'page_obj': page_obj,
        'user': request.user,
    }
    return render(request, 'blog/category.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = PostForm()
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'blog/create.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post.id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form, 'post': post,
        'user': request.user,
    }
    return render(request, 'blog/edit_post.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect("blog:profile", username=request.user.username)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    context = {
        'post': post,
        'user': request.user,
    }
    return render(request, 'blog/delete_post.html', context)


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
    return redirect("blog:profile", username=request.user.username)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    post = comment.post  # <-- ДОБАВИТЬ ЭТУ СТРОКУ
    if comment.author != request.user:
        return redirect("blog:profile", username=request.user.username)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form, 'post': post, 'comment': comment,
        'user': request.user,
    }
    return render(request, 'blog/edit_comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect("blog:profile", username=request.user.username)
    if request.method == 'POST':
        comment.delete()
    return redirect("blog:profile", username=request.user.username)


def profile(request, username):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = get_object_or_404(User, username=username)

    # Показываем ВСЕ посты автора, включая снятые с публикации
    post_list = Post.objects.filter(
        author=user
    ).select_related('category', 'location').order_by('-pub_date')

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user': request.user,
        'profile_user': user,
        'page_obj': page_obj,
        'post_list': page_obj.object_list
    }
    return render(request, 'blog/profile.html', context)
