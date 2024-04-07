from django.urls import path
from .views import store

urlpatterns = [
    path('trello_clone/tasks', store, name='store_tasks')
]