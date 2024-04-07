from rest_framework.decorators import api_view
from django.http import JsonResponse
from tasks.forms.create_task_form import CreateTaskFrom

# Create your views here.
@api_view(["POST"])
def store(request):
    task_form = CreateTaskFrom(request.json_body)
    
    if task_form.is_valid() == False:
        return JsonResponse(task_form.errors, status=422)
    
    task = task_form.save()
    
    return JsonResponse(task.serialize(serialize_relationships=['priority', 'step']), status=201)

@api_view(["PUT"])
def update_step(request):
    return