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
    
#class PreviousPageMiddleware:
 #   def __init__(self, get_response):
  #      self.get_response = get_response
#
 #   def __call__(self, request):
  #      if request.method == "GET":
            # Store the current path as the previous page (excluding login/logout pages)
            #excluded_paths = [reverse('RepairCafe:enter_password')]  # Add more if needed
            #if request.path not in excluded_paths:
                # Only store the page if it's not the same as the previous page
   #             if 'previous_page' not in request.session or request.session['previous_page'] != request.path:
    #                print(f"Storing previous_page: {request.get_full_path()}")  # Debugging
     #               request.session['previous_page'] = request.path
            #else:
             #   print(f"Excluded path: {request.path}")  # Debugging

      #  response = self.get_response(request)
       # return response