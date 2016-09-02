from __future__ import unicode_literals

import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.text import slugify

from blogoland.managers import PostManager, PostImageManager

TODAY = datetime.date.today

def get_slugified_file_name(filename):
    """
    Takes a filename string and slugify the file name and append its extension.
    This function will return a modified string like the next pattern:
    -- slugified-file-name.FILE_EXTENSION --
    """
    splitted_file_name = filename.split('.')
    slugified_file_name = slugify(splitted_file_name[0]) + '.' + splitted_file_name[1]
    del splitted_file_name
    return slugified_file_name

def get_image_path(instance, filename):
    """
    Builds a dynamic path for app images. This method takes an
    instance an builds the path like the next pattern:
    /blogoland/model_name/INSTANCE_SLUG/slugified-path.ext
    """
    return '{0}/{1}/{2}/{3}'.format(instance._meta.app_label,
                                    str(instance.post._meta.model_name),
                                    str(instance.post.pk),
                                    get_slugified_file_name(filename)
                                    )



class BaseModelInterface(models.Model):
    """
    Common attibutes for blogoland app models.
    """
    title =  models.CharField('Title', max_length=255)
    slug = models.SlugField('Slug', max_length=255, unique=True)

    class Meta:
        abstract = True


class SEOInterface(models.Model):
    """
    Search Engine Optimization Interface.
    """
    seo_title = models.CharField('SEO Title', max_length=70, blank=True, null=True)
    seo_description = models.CharField('SEO Meta Description', max_length=160, blank=True, null=True)
    seo_keywords = models.CharField('SEO Meta Keywords', max_length=160, blank=True, null=True)
    
    class Meta:
        abstract = True

    
@python_2_unicode_compatible
class Category(BaseModelInterface, SEOInterface):
    """
    Category model class.
    """

    class Meta:
        verbose_name = 'Categoty'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogoland:category_detail', kwargs={'category_slug': self.slug})


@python_2_unicode_compatible
class Post(BaseModelInterface, SEOInterface):
    """
    Main Post Class.
    """
    content = models.TextField('Description', blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True)
    
    creation_date = models.DateTimeField('Creation Date', auto_now_add=True)
    publication_date = models.DateField('Publication Date', default=TODAY)
    is_visible = models.BooleanField('Visible', default=True)

    objects = PostManager()


    class Meta:
        ordering = ['-publication_date', '-creation_date', 'slug']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.seo_title:
            self.seo_title = self.title
        if not self.seo_description:
            self.seo_description = strip_tags(self.content)[:160]
        return super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blogoland:post_detail', kwargs={'post_slug': self.slug})

    def is_public(self):
        """
        Check if public post.
        """
        now = timezone.now()
        return self.publication_date <= TODAY() and self.is_visible == True
    is_public.boolean = True
    is_public.short_description = 'Public'



@python_2_unicode_compatible
class PostImage(models.Model):
    """
    Image associated to Page object. 
    """
    IMG_TYPE_CHOICES = {
        ('thumbnail', 'Thumbnail Image'),
        ('detail', 'Detail Image'),
        ('gallery', 'Gallery Image'),
    }
    title =  models.CharField('Title', max_length=255)
    img_type =  models.CharField('Image Type', max_length=255, choices=IMG_TYPE_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to=get_image_path, max_length=255)
    post = models.ForeignKey(Post, related_name='image_set')

    objects = PostImageManager()

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.title