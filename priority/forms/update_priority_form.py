from priority.models import Priority
from django import forms


class UpdatePriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ["order", "name", "color"]

    order = forms.IntegerField(required=True)
    name = forms.CharField(max_length=255, required=True)
    color = forms.CharField(max_length=7, min_length=7, required=True)
