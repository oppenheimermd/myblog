from importlib.resources import path
from django.urls import path
from . import views
from .feeds import LastestPostFeed

# application namespace.  Allows us to organize URL's by application and use the
# 'app_name' when referring to it.
app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    #path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('feed/', LastestPostFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]