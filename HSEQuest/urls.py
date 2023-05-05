from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns

from HSEQuest.settings import DEBUG

urlpatterns = [
    path('', RedirectView.as_view(url='quest/', permanent=True)),
    path('quest/', include('quest.urls')),
    path('user/', include('user.urls')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

if DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
