from django.db import models
from trelloApi.helpers.default_models_field import DefaultModelsField


# Create your models here.
class User(DefaultModelsField):
    class Meta:
        db_table = "users"

    id = models.CharField(primary_key=True, editable=True)
