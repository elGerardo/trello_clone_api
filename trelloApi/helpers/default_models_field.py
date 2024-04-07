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

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(default=None, null=True)

    objects = AppManager()

    def serialize(self, serialize_relationships=[]):
        response = {}
        for field in self._meta.fields:
            field_value = getattr(self, field.name)
            if field.get_internal_type() == "ForeignKey":
                if field.name in serialize_relationships:
                    response[field.name] = field_value.serialize()
                    continue
                response[field.name + "_id"] = field_value.id
                continue
            response[field.name] = field_value

        return response
