from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:post_id>/', views.post_detail, name="post_detail"),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),  # ИСПРАВЛЕНО
    path('profile/<str:username>/', views.profile, name='profile'),
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/',
         views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/comment/',
         views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/comment/<int:comment_id>/edit/',
         views.edit_comment, name='edit_comment'),
    path('posts/<int:post_id>/comment/<int:comment_id>/delete/',
         views.delete_comment, name='delete_comment'),
]
