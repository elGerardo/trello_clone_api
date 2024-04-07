from django.urls import path
from .views import store

urlpatterns = [
    path('trello_clone/user', store, name='store_user')
]