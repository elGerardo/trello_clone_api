from django.http import JsonResponse
from rest_framework.decorators import api_view
from steps.forms.create_step_form import CreateStepForm
from steps.forms.update_step_form import UpdateStepForm
from django.shortcuts import get_object_or_404
from steps.models import Steps


@api_view(["POST", "GET"])
def crud_objects(request):
    if request.method == "POST":
        result = store(request=request)

    if request.method == "GET":
        result = getAll(request=request)

    return JsonResponse(result["response"], status=result["status"], safe=False)


def getAll(request):
    user = getattr(request, 'current_user', None)
    steps_with_tasks = Steps.objects.filter(user_id=user.id).prefetch_related('tasks_set').all()
    return {"response": steps_with_tasks.serialize(serialize_sets=['tasks_set']), "status": 200}

def store(request):
    user = getattr(request, "current_user", None)

    form = CreateStepForm(
        {**request.json_body, "is_default": False, "is_first": False, "user": user}
    )
    if form.is_valid() == False:
        return JsonResponse(form.errors, status=422)

    step = form.save()

    return {"response": step.serialize(), "status": 201}


@api_view(["PUT", "DELETE", "GET"])
def crud_object(request, step_id):
    if request.method == "PUT":
        result = update(request=request, step_id=step_id)

    if request.method == "DELETE":
        result = destroy(request=request, step_id=step_id)

    if request.method == "GET":
        result = find(request=request, step_id=step_id)

    return JsonResponse(result["response"], status=result["status"])


def update(request, step_id):
    user = getattr(request, "current_user", None)
    step = get_object_or_404(Steps, id=step_id, user_id=user.id)
    form = UpdateStepForm(request.json_body)
    if form.is_valid() == False:
        return {"response": form.errors, "status": 422}

    step.merge(form.cleaned_data).save()

    return {"response": step.serialize(), "status": 202}


def destroy(request, step_id):
    user = getattr(request, "current_user", None)

    step = get_object_or_404(Steps, id=step_id, user_id=user.id)
    step.delete()

    return {"response": {}, "status": 204}


def find(request, step_id):
    user = getattr(request, "current_user", None)

    step = get_object_or_404(Steps, id=step_id, user_id=user.id)

    return {"response": step.serialize(), "status": 200}
