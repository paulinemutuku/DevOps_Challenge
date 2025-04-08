from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

from .models import UserProfile


class UserProfileMiddleware(MiddlewareMixin):
    """
    Middleware to attach UserProfile to authenticated users in request
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        
        response = self.get_response(request)
        
        return response

    def process_request(self, request):
        """
        Attach userprofile to authenticated users
        """
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser) and request.user.is_authenticated:
            try:
                profile = request.user.userprofile
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(user=request.user)
                
        return True