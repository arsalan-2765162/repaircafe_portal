from django.urls import path
from RepairCafe import views
from .views import enter_password

app_name = 'RepairCafe'

urlpatterns = [
        path('', views.index, name='index'),
	path('reset_data', views.reset_data, name='reset_data'),
        path('repair/<str:repairNumber>',views.repair_item,name='repair_item'),
        path('complete/<str:repairNumber>',views.complete_ticket,name='complete_ticket'),
        path('mark_incomplete_ticket/<str:repairNumber>/', views.mark_incomplete_ticket, name='mark_incomplete_ticket'),
        path('main_queue', views.main_queue, name='main_queue'),
        path('waiting_list', views.waiting_list, name='waiting_list'),
        path('checkout_queue', views.checkout_queue, name='checkout_queue'),
        path('accept_ticket/<str:repairNumber>/',views.accept_ticket, name='accept_ticket'),
        path('repair_ticket/<str:repairNumber>/',views.repair_ticket,name='repair_ticket'),
        path('delete-ticket/<str:repairNumber>/',views.delete_ticket,name='delete_ticket'),
        path('checkout_ticket/<str:repairNumber>/',views.checkout_ticket,name='checkout_ticket'),
        path('enter_password/', views.enter_password, name='enter_password'),
        path('house_rules/', views.house_rules, name='house_rules'),
        path('checkout',views.checkout,name='checkout'),
        path('checkout_success',views.checkout_success,name='checkout_success')

]
