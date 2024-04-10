from django.urls import path
from .views import store, crud_object

urlpatterns = [
    path('trello_clone/priority', store, name='store_priority'),
    path('trello_clone/priority/<str:priority_id>', crud_object, name='crud_object_priority'),
]