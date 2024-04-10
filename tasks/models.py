import uuid
from django.db import models
from trelloApi.helpers.default_models_field import DefaultModelsField
from user.models import User
from priority.models import Priority
from steps.models import Steps


# Create your models here.
class Tasks(DefaultModelsField):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        unique=False, max_length=255, default=None, editable=True, null=True
    )
    description = models.TextField(unique=False, default=None, editable=True, null=True)
    secuence = models.IntegerField(null=False, editable=True, unique=False)
    is_finished = models.BooleanField(null=False, editable=True, default=False)

    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    step = models.ForeignKey(Steps, on_delete=models.CASCADE)

    class Meta:
        db_table = "tasks"
