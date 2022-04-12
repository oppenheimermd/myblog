from importlib.resources import path
from django.urls import path
from . import views

# application namespace.  Allows us to organize URL's by application and use the
# 'app_name' when referring to it.
app_name = 'blog'

urlpatterns = [
    # post views
    #path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail'),
]