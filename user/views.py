from rest_framework.decorators import api_view
from user.forms.create_user_form import CreateUserForm
from steps.forms.create_step_form import CreateStepForm
from priority.forms.create_priority_form import CreatePriorityForm
from django.http import JsonResponse
from priority.default_data.default_data import get_default_data as get_priority_data
from steps.default_data.default_data import get_default_data as get_step_data


# Create your views here.
@api_view(["POST"])
def store(request):
    user_form = CreateUserForm(request.json_body)

    if user_form.is_valid() == False:
        return JsonResponse(user_form.errors, status=422)

    user = user_form.save()

    priorities = []

    priority_data = get_priority_data()
    for priority_item in priority_data:
        priority_item["user"] = user
        priority_item = CreatePriorityForm(priority_item)
        if priority_item.is_valid() == False:
            return JsonResponse(priority_item.errors, status=422)
        model = priority_item.save()
        priorities.append(model.serialize())

    steps = []

    step_data = get_step_data()
    for step_item in step_data:
        step_item["user"] = user
        step_item = CreateStepForm(step_item)
        if step_item.is_valid() == False:
            return JsonResponse(step_item.errors, status=422)
        model = step_item.save()
        steps.append(model.serialize())

    return JsonResponse(
        {**user.serialize(), "steps": steps, "priorities": priorities}, status=201
    )
