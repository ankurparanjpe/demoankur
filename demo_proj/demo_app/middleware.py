from django.template.response import TemplateResponse


class RequestLoggerMiddleware:
    def __init__(self, get_response):
        print('Before intializing the server')
        self.get_response = get_response
        print('After initializing the server', get_response)

    def __call__(self, request):
        # Log the request method and URL
        print(f'Request: {request.method} {request.get_full_path()}')
        print('Before any method is called')

        # Call the next middleware or view
        response = self.get_response(request)
        print('After any method is called')
        return response
    
    def process_view(request, view_func, *view_args, **view_kwargs):
        # This code is executed just before the view is called
        print('process_view')

    def process_exception(request, *exception):
        # This code is executed if an exception is raised
        print('Exception')

    def process_template_response(self, request, response):
        #Runs when there is "TemplateResponse" in return method
        print('Template is rendered')
        return response


# def simple_middleware(get_response):
#     # One-time configuration and initialization.

#     def middleware(request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#         print('Before request')

#         response = get_response(request)
#         print('After request')

#         # Code to be executed for each request/response after
#         # the view is called.

#         return response

#     return middleware