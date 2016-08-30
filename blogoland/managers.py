
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