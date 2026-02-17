from django.conf import settings
from django.conf.urls import handler403, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from pages import views as pages_views
from users.views import password_change, registration

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('users.urls')),
    path('registration/', registration, name='registration'),
    path('password/change/', password_change, name='password_change'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

handler403 = 'pages.views.csrf_failure'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
