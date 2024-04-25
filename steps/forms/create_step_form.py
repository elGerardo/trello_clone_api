from django import forms
from steps.models import Steps
from user.models import User

class CreateStepForm(forms.ModelForm):
    class Meta:
        model = Steps
        fields = ["name", "is_default", "is_first", "order", "user"]

    name = forms.CharField(max_length=255, required=True)
    is_default = forms.BooleanField(required=False)
    is_first = forms.BooleanField(required=False)
    order = forms.IntegerField(required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all())
