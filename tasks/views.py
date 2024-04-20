from rest_framework.decorators import api_view
from django.http import JsonResponse
from tasks.forms.create_task_form import CreateTaskFrom
from tasks.forms.update_task_form import UpdateTaskForm
from .models import Tasks
from django.shortcuts import get_object_or_404
from steps.models import Steps
from tasks.forms.bulk_update_task_form import BulkUpdateTaskForm
from django_bulk_load import bulk_update_models


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


@api_view(["PUT"])
def bulk_update(request):
    user = getattr(request, "current_user", None)

    if not isinstance(request.json_body, list):
        return JsonResponse({"messsage": ["Payload must be an array"]})
    
    bulk_models = []
    bulk_response = []

    for index, item in enumerate(request.json_body):
        form = BulkUpdateTaskForm({**item, "user_id": user.id})
         
        if form.is_valid() == False:
            return JsonResponse({index: form.errors}, status=422)
        
        model = form.cleaned_data["task"].merge(form.cleaned_data)
        bulk_models.append(model)
        bulk_response.append(model.serialize())

    bulk_update_models(models=bulk_models, return_models=False, update_field_names=["step_id", "secuence"])
    return JsonResponse(bulk_response, status=201, safe=False)
