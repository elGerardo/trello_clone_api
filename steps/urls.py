from django.urls import path
from .views import crud_objects, crud_object

urlpatterns = [
    path('trello_clone/steps', crud_objects, name='crud_objects_step'),
    path('trello_clone/steps/<str:step_id>', crud_object, name='crud_object_steps'),
]