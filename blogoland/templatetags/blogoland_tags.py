# *-* coding=utf-8 *-*
from django import template
from django.conf import settings
from django.utils.html import format_html, strip_tags
from django.utils.text import capfirst

from blogoland.confs import DEFAULT_DATE_FORMAT
from blogoland.models import Post

register = template.Library()

DATE_FORMAT = getattr(settings, 'BLOGOLAND_DATE_FORMAT', DEFAULT_DATE_FORMAT)

# Helper function
def build_img_tag(img):
    """
    Build a HTML Img TAG with the given img object.
    """
    img_tag = '<img src="{0}" alt="{1}" />'.format(img.image.url, img.title)
    return mark_safe(img_tag)


@register.simple_tag(takes_context=True)
def post_title(context):    
    """
    Returns the title with capfirst filter applied. If post isn't public
    this tag will append a '[DRAFT]' string and output the final title.
    """
    post = context['object']
    title = capfirst(post.title)

    if not post.is_public():
        title = '[DRAFT] %s' % title 

    return title
    
@register.simple_tag(takes_context=True)
def post_date(context):
    """
    Returns the formated date. 
    Default: '%d-%m-%Y'
    """
    post = context['object']
    return post.publication_date.strftime(DATE_FORMAT)

@register.simple_tag(takes_context=True)
def post_content(context):
    """
    Check if the given instance wrapped in the context is a Post one. Then 
    parse the content of the post to HTML.
    """
    try:
        post = context['object']
        if isinstance(post, Post):
            return format_html(post.content)
    except: 
        return ''


@register.simple_tag(takes_context=True)
def detail_image(context):
    """
    Render the first detail image of the Post
    """
    try:
        obj = context['object']
        img = obj.image_set.filter(img_type='detail').first()
        img_tag = build_img_tag(img)
        return img_tag
    except:
        return

@register.simple_tag(takes_context=True)
def thumbnail_image(context):
    """
    Render the first thumbnail image of the Post
    """
    try:
        obj = context['object']
        img = obj.image_set.filter(img_type='thumbnail').first()
        img_tag = build_img_tag(img)
        return img_tag
    except:
        return

@register.simple_tag(takes_context=True)
def get_gallery_images(context):
    """
    Returns a list of img related objects selected as 'gallery'
    """
    try:
        obj = context['object']
        return obj.image_set.filter(img_type='gallery')
    except:
        return []