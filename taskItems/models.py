import uuid
from django.db import models
from trelloApi.helpers.default_models_field import DefaultModelsField
from priority.models import Priority
from steps.models import Steps
from tasks.models import Tasks


# Create your models here.
class TaskItems(DefaultModelsField):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        unique=False, max_length=255, default=None, editable=True, null=True
    )
    description = models.TextField(unique=False, default=None, editable=True, null=True)
    order = models.IntegerField(null=False, editable=True, unique=False)

    # Relationships
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    step = models.ForeignKey(Steps, on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)

    class Meta:
        db_table = 'task_items'

