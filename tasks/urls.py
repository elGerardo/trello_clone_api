from django.urls import path
from .views import store, crud_object, update_task_step

urlpatterns = [
    path('trello_clone/tasks', store, name='store_task'),
    path('trello_clone/tasks/<str:task_id>', crud_object, name='crud_object_task'),
    path('trello_clone/tasks/<str:task_id>/step/<str:step_id>', update_task_step, name='update_task_step')
]