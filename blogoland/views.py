# -*- coding:utf8 -*-
from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.list import MultipleObjectMixin

from blogoland.models import Post, Category



class PostListView(ListView):
    """
    List the Post model.
    """
    model = Post

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return Post.objects.all()
        return Post.objects.get_public_posts()

    def get_template_names(self):
        return [
                "blogoland/post_list.html",
                ] 


class PostDetailView(DetailView):
    """
    Detail the Post model.
    """
    model = Post

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return Post.objects.all()
        return Post.objects.get_public_posts()
    
    def get_object(self):
        post_qs = self.get_queryset()
        post_slug = self.kwargs.get('post_slug', None)
        try:
            post = post_qs.get(slug=post_slug)
        except:
            raise Http404()
        return post

    def get_template_names(self):
        return [
                "blogoland/post_{0}.html".format(self.kwargs.get('post_slug')),
                "blogoland/post_detail.html",
                ] 
  

class CategoryDetailView(DetailView):
    """
    Returns the Detail of Category and the QuerySet of post related to 
    Category and filter if user is or not logged in admin.
    """
    model = Category

    def get_queryset(self, *args, **kwargs):
        return Category.objects.all()

    def get_object(self):
        category_qs = self.get_queryset()
        category_slug = self.kwargs.get('category_slug', None)
        try:
            category = category_qs.get(slug=category_slug)
        except:
            raise Http404()
        return category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        category = self.get_object()

        if self.request.user.is_staff:
            category_posts = category.post_set.all()
        else: 
            category_posts = category.post_set.get_public_posts()

        context['object_list'] = category_posts
        return context

    def get_template_names(self):
        return [
                "blogoland/category_{0}.html".format(self.kwargs.get('category_slug')),
                "blogoland/category_detail.html",
                ] 
  