from uuid import uuid4

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Blog, Comments, Topic


def invalidate_home_cache():
    cache.set("home:cache_version", uuid4().hex, timeout=None)


@receiver([post_save, post_delete], sender=Blog)
@receiver([post_save, post_delete], sender=Topic)
@receiver([post_save, post_delete], sender=Comments)
@receiver([post_save, post_delete], sender=User)
def invalidate_home_cache_on_change(sender, **kwargs):
    invalidate_home_cache()