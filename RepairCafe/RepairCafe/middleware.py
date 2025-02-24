from django.shortcuts import redirect
from django.urls import reverse


class PasswordProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access to admin URLs
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # Allow access to the password entry page itself
        if request.path == reverse('RepairCafe:enter_password'):
            return self.get_response(request)

        # Check if password verified
       # if request.session.get('sessionpassword') not in ["undefined", "visitor", "repairer", "volunteer"]:
        #    return redirect('RepairCafe:enter_password')
        
        return self.get_response(request)