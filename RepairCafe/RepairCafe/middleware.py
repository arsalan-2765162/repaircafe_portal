from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class PasswordProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path == reverse('enter_password'):
            return self.get_response(request)
        
        if not request.session.get('preset_password_verified'):
            return redirect('enter_password')
        
        return self.get_response(request)