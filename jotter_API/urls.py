from django.conf.urls import url
import jotter_API.views as views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^auth/$', views.CustomObtainAuthToken.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/note/', views.NoteView.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/image/', views.ImageView.as_view()),
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
