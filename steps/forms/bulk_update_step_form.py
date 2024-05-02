from django import forms
from steps.models import Steps

class BulkUpdateStepForm(forms.ModelForm):
    class Meta:
        model = Steps
        fields = ["order"]

    order = forms.IntegerField(required=True)
    id = forms.CharField(required=True)

    user_id = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()

        step_id = cleaned_data.get("id")
        user_id = cleaned_data.get("user_id")

        step = Steps.objects.filter(id=step_id, user_id=user_id).first()
        if step is None:
            raise forms.ValidationError({"step_id": ["Step Id does not belong to user"]})
        
        cleaned_data["step"] = step

        return cleaned_data

