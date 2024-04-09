from django.http import JsonResponse
from trelloApi.settings import MIDDLEWARE_URL_SKIP
from user.models import User

class HeaderUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path in MIDDLEWARE_URL_SKIP:
            return response
        
        x_user_id =  request.META.get('HTTP_X_USER_ID')

        if x_user_id is None:
            return JsonResponse({ "message": "Missing X-USER-ID" }, status=401)
        
        user_exist = User.objects.filter(id=x_user_id).first()

        if user_exist is None:
            return JsonResponse({ "message": "X-USER-ID Not exist" }, status=404)
        
        return response