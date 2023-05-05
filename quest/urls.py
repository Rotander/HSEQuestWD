from . import views
from django.urls import re_path


urlpatterns = [
    re_path(r'^catalog', views.catalog, name='catalog'),
    re_path(r'^play', views.new_play, name='new_play'),
    re_path(r'^feedback', views.feedback, name='feedback'),
    re_path(r'^aboutus', views.aboutus, name='aboutus'),
    re_path(
        r'^export/csv/finished_users/$',
        views.export_finished_users_csv,
        name='export_finished_users_csv',
    ),
    re_path(
        r'^export/csv/users_pages/$',
        views.export_users_pages_csv,
        name='export_users_pages_csv',
    ),
    re_path(
        r'^export/csv/feedback/$',
        views.export_feedback_csv,
        name='export_feedback_csv'
    ),
    re_path(r'^', views.index, name='index'),
]
