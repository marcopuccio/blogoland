# *-* coding=utf-8 *-*
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.html import format_html, mark_safe, strip_tags
from django.utils.text import capfirst, Truncator

from blogoland.confs import DEFAULT_DATE_FORMAT
from blogoland.models import Post, Category

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
def post_excerpt(context, word_limit=10):
    """
    Returns the excerpt of the post. Strips the HTML tags and truncate the
    words by the given limit.
    """
    post = context['object']
    return Truncator(strip_tags(post.content)).words(word_limit)

@register.simple_tag(takes_context=True)
def post_detail_image(context):
    """
    Render the first detail image of the Post
    """
    try:
        post = context['object']
        img = post.image_set.get_last_img_type('detail')
        img_tag = build_img_tag(img)
        return img_tag
    except:
        return

@register.simple_tag(takes_context=True)
def post_thumbnail_image(context):
    """
    Render the first thumbnail image of the Post
    """
    try:
        post = context['object']
        img = post.image_set.get_last_img_type('thumbnail')
        img_tag = build_img_tag(img)
        return img_tag
    except:
        return

@register.simple_tag(takes_context=True)
def get_post_gallery_images(context):
    """
    Returns a list of img related objects selected as 'gallery'
    """
    try:
        post = context['object']
        return post.image_set.filter(img_type='gallery')
    except:
        return []

@register.simple_tag
def get_latest_posts(post_limit=None):
    """
    Returns a Qs of the latest public post sliced by limit.
    """
    return Post.objects.get_public_posts()[:post_limit]

@register.simple_tag
def get_category_list(cat_limit=None):
    """
    Return a QuerySet of Category object and can be sliced by limit.
    """
    return Category.objects.all()[:cat_limit]

@register.simple_tag(takes_context=True)
def social_media_image_url(context):
    """
    Returns the thumbnail URL built to be used in Open Graph tags.
    """
    site = Site.objects.get_current()
    try:
        post = context['object']
        img = post.image_set.get_last_img_type('thumbnail')
        return 'http://{0}{1}'.format(site.domain, img.image.url)
    except:
        return

@register.simple_tag(takes_context=True)
def social_media_post_url(context):
    """
    Returns the post's URL built to be used on Open Graph and Twitter Card.
    """
    site = Site.objects.get_current()
    try:
        post = context['object']
        return 'http://{0}{1}'.format(site.domain, post.get_absolute_url())
    except:
        return

@register.inclusion_tag('blogoland/snippets/paginator.html', takes_context=True)
def paginator(context):
    """
    Template tag to easy including the pagination in template. This tag, only
    pass the context to the default template.
    """
    return context