from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^register', views.signup, name='signup'),
    re_path(r'^login', views.signin, name='signin'),
    re_path(r'^logout', views.site_logout, name='logout'),
    re_path(r'^presents', views.presents, name='presents'),
    re_path(r'^report', views.report, name='report'),
    re_path(r'^$', views.profile, name="profile"),
]
