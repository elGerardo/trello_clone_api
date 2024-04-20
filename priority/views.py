from django.http import JsonResponse
from rest_framework.decorators import api_view
from priority.forms.create_priority_form import CreatePriorityForm
from priority.forms.update_priority_form import UpdatePriorityForm
from django.shortcuts import get_object_or_404
from priority.models import Priority


@api_view(["POST", "GET"])
def crud_objects(request):
    if request.method == "POST":
        result = store(request=request)

    if request.method == "GET":
        result = getAll(request=request)
    print("alskdhjaskl")
    return JsonResponse(result["response"], status=result["status"], safe=False)

def store(request):
    user = getattr(request, "current_user", None)

    form = CreatePriorityForm({**request.json_body, "user": user})
    if form.is_valid() == False:
        return JsonResponse(form.errors, status=422)

    priority = form.save()

    return {"response": priority.serialize(), "status": 201}

def getAll(request):
    user = getattr(request, "current_user", None)

    priorities = Priority.objects.filter(user_id=user.id)

    return {"response": priorities.serialize(aliases_values={"id": "value", "name": "label"}), "status": 200}


@api_view(["GET", "PUT", "DELETE"])
def crud_object(request, priority_id):
    if request.method == "PUT":
        result = update(request=request, priority_id=priority_id)

    if request.method == "DELETE":
        result = destroy(request=request, priority_id=priority_id)

    if request.method == "GET":
        result = find(request=request, priority_id=priority_id)

    return JsonResponse(result["response"], status=result["status"])


def update(request, priority_id):
    user = getattr(request, "current_user", None)

    priority = get_object_or_404(Priority, id=priority_id, user_id=user.id)

    form = UpdatePriorityForm(request.json_body)
    if form.is_valid() == False:
        return {"response": form.errors, "status": 422}

    priority.merge(form.cleaned_data).save()

    return {"response": priority.serialize(), "status": 202}


def destroy(request, priority_id):
    user = getattr(request, "current_user", None)

    priority = get_object_or_404(Priority, id=priority_id, user_id=user.id)
    priority.delete()

    return {"response": {}, "status": 204}


def find(request, priority_id):
    user = getattr(request, "current_user", None)

    priority = get_object_or_404(Priority, id=priority_id, user_id=user.id)

    return {"response": priority.serialize(), "status": 200}
