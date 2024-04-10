from typing import Any
from django import forms
from steps.models import Steps

class UpdateStepForm(forms.ModelForm):
    class Meta:
        model = Steps
        fields = ["name", "order"]

    name = forms.CharField(max_length=255, required=True)
    order = forms.IntegerField(required=True)