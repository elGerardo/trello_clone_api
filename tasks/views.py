from rest_framework.decorators import api_view
from django.http import JsonResponse
from tasks.forms.create_task_form import CreateTaskFrom
from tasks.forms.update_task_form import UpdateTaskForm
from .models import Tasks
from django.shortcuts import get_object_or_404
from steps.models import Steps


# Create your views here.
@api_view(["POST"])
def store(request):
    task_form = CreateTaskFrom(
        {**request.json_body, "user_id": request.META.get("HTTP_X_USER_ID")}
    )

    if task_form.is_valid() == False:
        return JsonResponse(task_form.errors, status=422)

    task = task_form.save()

    return JsonResponse(
        task.serialize(serialize_relationships=["priority", "step"]), status=201
    )


@api_view(["PUT", "DELETE", "GET"])
def crud_object(request, task_id):
    user_id = request.META.get("HTTP_X_USER_ID")
    if request.method == "PUT":
        result = update(request=request, task_id=task_id, user_id=user_id)

    if request.method == "DELETE":
        result = destroy(request=request, task_id=task_id, user_id=user_id)

    if request.method == "GET":
        result = find(request=request, task_id=task_id, user_id=user_id)

    return JsonResponse(result["response"], status=result["status"])


def find(request, task_id, user_id):
    task = get_object_or_404(Tasks, id=task_id, user_id=user_id)
    return {"response": task.serialize(), "status": 200}


def update(request, task_id, user_id):
    task = get_object_or_404(Tasks, id=task_id, user_id=user_id)

    form = UpdateTaskForm({**request.json_body, "user_id": user_id})
    if form.is_valid() == False:
        return {"response": form.errors, "status": 422}

    task.merge(form.cleaned_data)
    task.save()

    return {"response": task.serialize(), "status": 202}


def destroy(request, task_id, user_id):
    task = get_object_or_404(Tasks, id=task_id, user_id=user_id)
    task.delete()

    return {"response": {}, "status": 204}


@api_view(["PUT"])
def update_task_step(request, task_id, step_id):
    user_id = request.META.get("HTTP_X_USER_ID")

    task = get_object_or_404(Tasks, id=task_id, user_id=user_id)
    step = get_object_or_404(Steps, id=step_id, user_id=user_id)

    task.step = step
    task.save()

    return JsonResponse(task.serialize("steps"), status=201)
