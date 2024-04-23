from django import forms
from priority.models import Priority
from user.models import User


class CreatePriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ["name", "color", "is_default", "is_first", "user"]

    name = forms.CharField(max_length=255, required=True)
    color = forms.CharField(max_length=255, required=True)
    is_default = forms.BooleanField(required=False)
    is_first = forms.BooleanField(required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all())
