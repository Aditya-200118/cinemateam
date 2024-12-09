from django.utils.deprecation import MiddlewareMixin

class RemoveCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith('/accounts/') or request.path.startswith('/logout/') or request.path.startswith('/admin/') or request.path.startswith("/booking/checkout_process/"): 
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
