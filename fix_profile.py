def profile(request, username):
    user = get_object_or_404(User, username=username)
    
    # Автор видит все свои посты (включая отложенные и неопубликованные)
    if request.user == user:
        posts = Post.objects.filter(author=user).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
    else:
        # Другие пользователи видят только опубликованные
        posts = Post.objects.filter(
            author=user,
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/profile.html', {
        'profile_user': user,
        'page_obj': page_obj
    })
