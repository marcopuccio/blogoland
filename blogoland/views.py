# -*- coding:utf8 -*-
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.list import MultipleObjectMixin

from blogoland.confs import DEFAULT_PAGINATION
from blogoland.models import Post, Category


PAGINATION = getattr(settings, 'BLOGOLAND_PAGINATION', DEFAULT_PAGINATION)


class PostListView(ListView):
    """
    List the Post model.
    """
    model = Post
    paginate_by = PAGINATION

    def get_queryset(self, *args, **kwargs):
        """
        Returns QuerySet of Post
        """
        if self.request.user.is_staff:
            return Post.objects.all()
        return Post.objects.get_public_posts()

    def get_template_names(self):
        """
        Returns template selection hierarchy.
        """
        return [
                "blogoland/post_list.html",
                ] 


class PostDetailView(DetailView):
    """
    Detail the Post model.
    """
    model = Post

    def get_queryset(self, *args, **kwargs):
        """
        Returns QuerySet of Post
        """
        if self.request.user.is_staff:
            return Post.objects.all()
        return Post.objects.get_public_posts()
    
    def get_object(self):
        """
        Returns the Post detail by the given slug requestself.
        """
        post_qs = self.get_queryset()
        post_slug = self.kwargs.get('post_slug', None)
        try:
            post = post_qs.get(slug=post_slug)
        except:
            raise Http404()
        return post

    def get_template_names(self):
        """
        Returns template selection hierarchy.
        """
        return [
                "blogoland/post_{0}.html".format(self.kwargs.get('post_slug')),
                "blogoland/post_detail.html",
                ] 
  

class CategoryPostListView(ListView):
    """
    Returns the Detail of Category and the QuerySet of Posts related to 
    Category and filter if user is or not logged in admin.
    """
    model = Post
    paginate_by = PAGINATION

    def get_queryset(self, *args, **kwargs):
        """
        Return the Post QuerySet filtered by the category requested,
        """
        category = self.get_object()
        if self.request.user.is_staff:
            return Post.objects.filter(category=category)
        return Post.objects.get_public_posts().filter(category=category)

    def get_object(self):
        """
        Get the category by the given slug or raise 404
        """
        category_slug = self.kwargs.get('category_slug', None)
        try:
            category = Category.objects.get(slug=category_slug)
        except:
            raise Http404()
        return category

    def get_context_data(self, **kwargs):
        """
        Adds the category object to the context.
        """
        context = super(CategoryPostListView, self).get_context_data(**kwargs)
        category = self.get_object()
        context['object'] = category
        return context

    def get_template_names(self):
        """
        Returns template selection hierarchy.
        """
        return [
                "blogoland/category_{0}_list.html".format(self.kwargs.get('category_slug')),
                "blogoland/category_post_list.html",
                ] 
