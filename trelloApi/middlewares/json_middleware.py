import json
from django.http import JsonResponse

class JsonMiddleware:
    """Middleware that parses JSON request body and sets it as a QueryDict
    in the request object.
    """
    invalid_json_http_status = 400
    invalid_json_response = {'error': 'Invalid JSON request'}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ('GET', 'POST') \
                and (content_type := request.META.get('CONTENT_TYPE')) \
                and 'application/json' in content_type.lower():
            try:
                request.json_body = json.loads(request.body)
            except ValueError:
                return JsonResponse(
                    self.invalid_json_response,
                    status=self.invalid_json_http_status)
            
        return self.get_response(request)