# -*- coding:utf8 -*-

from django.conf.urls import url, include

from blogoland.views import PostListView, PostDetailView, CategoryPostListView

app_name = 'blogoland'
urlpatterns = [
    url(r'^$', PostListView.as_view(), name='post_list'),
    url(r'^(?P<post_slug>[-\w]+)/$', PostDetailView.as_view(), name='post_detail'),
    url(r'^category/(?P<category_slug>[-\w]+)/$', CategoryPostListView.as_view(), name='category_post_list'),
]