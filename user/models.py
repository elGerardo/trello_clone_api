from django.db import models
from trelloApi.helpers.default_models_field import DefaultModelsField


# Create your models here.
class User(DefaultModelsField):
    id = models.CharField(primary_key=True, editable=False)

    class Meta:
        db_table = "users"
