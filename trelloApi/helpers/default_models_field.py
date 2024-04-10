from django.db import models
from django.db.models import Manager, QuerySet
from django.utils import timezone


class AppQuerySet(QuerySet):
    def delete(self):
        self.update(deleted_at=timezone.now())

    def serialize(self, serialize_sets=[]):
        items = []
        models = self

        for model in models:
            item = {}
            for field in model._meta.fields:
                field_value = getattr(model, field.name)
                if field.get_internal_type() == "ForeignKey":
                    item[field.name + "_id"] = field_value.id
                    continue
                item[field.name] = field_value

            for serialize_set in serialize_sets:
                item_sets = []
                for set_item in getattr(model, serialize_set).all():
                    item_set = {}
                    for model_item in set_item._meta.fields:
                        field_value = getattr(set_item, model_item.name)
                        if model_item.get_internal_type() == "ForeignKey":
                            item_set[model_item.name + "_id"] = field_value.id
                            continue
                        item_set[model_item.name] = field_value
                    item_sets.append(item_set)

                item[serialize_set] = item_sets

            items.append(item)
        return items


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

    def merge(self, payload={}):
        for key, value in payload.items():
            setattr(self, key, value)
        return self
