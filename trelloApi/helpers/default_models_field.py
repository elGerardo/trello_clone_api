from django.db import models
from django.db.models import Manager, QuerySet
from django.utils import timezone

class AppQuerySet(QuerySet):
    def delete(self):
        self.update(deleted_at=timezone.now())

class AppManager(Manager):
    def get_queryset(self):
        return AppQuerySet(self.model, using=self._db).exclude(deleted_at__isnull=False)

class DefaultModelsField(models.Model):
    class Meta:
        abstract = True
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None)

    objects = AppManager()
