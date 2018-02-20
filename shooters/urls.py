from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'template_name': 'registration/logged_out.html'}, name='logout'),
    path('admin/', admin.site.urls),
    path('ranking', include('ranking.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
