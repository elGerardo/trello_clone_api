import uuid
from django.db import models
from trelloApi.helpers.default_models_field import DefaultModelsField
from user.models import User


# Create your models here.
class Steps(DefaultModelsField):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(null=False, max_length=255, editable=True, unique=False)
    is_default = models.BooleanField(null=False, editable=True, unique=False)
    is_first = models.BooleanField(null=False, editable=True, unique=False)
    order = models.IntegerField(null=False, editable=True, unique=False)

    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "steps"
