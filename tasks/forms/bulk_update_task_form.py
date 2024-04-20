from django import forms
from tasks.models import Tasks
from steps.models import Steps

class BulkUpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["secuence", "step"]

    id = forms.CharField(max_length=255, required=True)
    secuence = forms.IntegerField(required=True)
    user_id = forms.CharField(required=True)
    step_id = forms.CharField(required=True)

    step = forms.ModelChoiceField(queryset=Steps.objects.all(), required=False)


    def clean(self):
        cleaned_data = super().clean()

        task_id = cleaned_data.get("id")
        user_id = cleaned_data.get("user_id")
        step_id = cleaned_data.get("step_id")

        task = Tasks.objects.filter(id=task_id, user_id=user_id).first()
        if task is None:
            raise forms.ValidationError({"id": ["Task Id does not belong to user"]})
        
        step = Steps.objects.filter(id=step_id, user_id=user_id).first()
        if step is None:
            raise forms.ValidationError({"step_id": ["Step Id does not belong to user"]})
        
        cleaned_data["step"] = step
        cleaned_data["task"] = task

        return cleaned_data
