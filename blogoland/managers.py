
import datetime

from django.db import models


class PostManager(models.Manager):
    """
    Manager for Post objects.
    """
    def get_public_posts(self, *args, **kwargs):
        """
        Returns public posts.
        """
        return self.get_queryset(*args, **kwargs).filter(is_visible=True, publication_date__lte=datetime.date.today())


class PostImageManager(models.Manager):
    """
    Manager for PostImage objects.
    """
    def get_last_img_type(self, img_type):
        """
        Returns the last image added fitered by type.
        """
        return self.get_queryset().filter(img_type=img_type).last()