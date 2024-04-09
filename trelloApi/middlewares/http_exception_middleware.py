from django.http import JsonResponse

class HttpExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 500 and not isinstance(response, JsonResponse):
            return JsonResponse({
                'message': 'Server Error' 
            }, status=500)

        if response.status_code == 404 and not isinstance(response, JsonResponse):
            return JsonResponse({
                'message': 'Row Not Found'
            }, status=404)

        return response