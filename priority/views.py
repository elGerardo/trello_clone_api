from django.http import JsonResponse
from rest_framework.decorators import api_view
from priority.forms.create_priority_form import CreatePriorityForm
from priority.forms.update_priority_form import UpdatePriorityForm
from django.shortcuts import get_object_or_404
from priority.models import Priority


@api_view(["POST"])
def store(request):
    user = getattr(request, "current_user", None)

    form = CreatePriorityForm({**request.json_body, "user": user})
    if form.is_valid() == False:
        return JsonResponse(form.errors, status=422)

    priority = form.save()

    return JsonResponse(priority.serialize(), status=201)


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
