from django.shortcuts import redirect
from django.urls import reverse
from django.urls import resolve


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
        if not request.user.is_authenticated or not request.user.activerole:
            return redirect(reverse('RepairCafe:enter_password'))

        return self.get_response(request)


'''class PreviousPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "GET":
            # Resolve the current view function
            view_func = resolve(request.path).func

            # Check if the view requires role-based authentication
            if not hasattr(view_func, 'role_based_authentication'):
                if 'previous_page' not in request.session or request.session['previous_page'] != request.path:
                    print(f"Storing previous_page: {request.path}")  # Debugging
                    request.session['previous_page'] = request.path

        response = self.get_response(request)
        return response'''