from django.urls import path
from .views import crud_objects, crud_object

urlpatterns = [
    path('trello_clone/priority', crud_objects, name='crud_objects_priority'),
    path('trello_clone/priority/<str:priority_id>', crud_object, name='crud_object_priority'),
]