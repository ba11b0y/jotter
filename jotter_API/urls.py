from django.conf.urls import url
import jotter_API.views as views

urlpatterns = [
    url(r'^auth/$', views.CustomObtainAuthToken.as_view()),
    url(r'user/(?P<pk>[0-9]+)/', views.NoteView.as_view()),
    ]