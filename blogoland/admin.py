# -*- coding:utf8 -*-

from django_summernote.admin import SummernoteModelAdmin

from django.contrib import admin

from blogoland.models import Post, PostImage, Category


class PostImageInline(admin.TabularInline):
    """
    Stack inline choice items to be displayed in Page Admin Panel
    """
    model = PostImage 
    extra = 1


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Customizing Page Model representation in Django Admin
    """
    fieldsets = [
            ('SEO', {
            'fields': [
                'seo_title',
                'seo_description',
                'seo_keywords',
            ],
            'classes': [
                'collapse',
                ]
            }),
            (None, {
                'fields': [
                    'title',
                    'slug',
                    ('publication_date','is_visible'),
                    'category',
                    'content',
                    ]
                })
            ]

    prepopulated_fields = {'slug': ('title',)}
    inlines = [PostImageInline]
    list_display = (
            'id',
            'title',
            'slug',
            'is_public',
            'is_visible',
            'publication_date',
            )
    list_display_links = ('id', 'title',)
    list_filter = ('publication_date', 'is_visible',  'creation_date',)
    search_fields = ['title', 'pk']

@admin.register(Category)
class CategoryAdmin(SummernoteModelAdmin):
    """
    Customizing Page Model representation in Django Admin
    """
    fieldsets = [
            ('SEO', {
            'fields': [
                'seo_title',
                'seo_description',
                'seo_keywords',
            ],
            'classes': [
                'collapse',
                ]
            }),
            (None, {
                'fields': [
                    'title',
                    'slug',
                    ]
                })
            ]

    prepopulated_fields = {'slug': ('title',)}
    list_display = (
            'id',
            'title',
            'slug',
            )
    list_display_links = ('id', 'title',)
    search_fields = ['title', 'pk']
