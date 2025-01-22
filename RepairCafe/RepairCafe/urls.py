from django.urls import path
from RepairCafe import views
from .views import enter_password

app_name = 'RepairCafe'

urlpatterns = [
        path('', views.index, name='index'),
	path('reset_data', views.reset_data, name='reset_data'),
        path('repair/<int:repairNumber>',views.repair_item,name='repair_item'),
        path('complete/<int:repairNumber>',views.complete_ticket,name='complete_ticket'),
        path('mark_incomplete_ticket/<int:repairNumber>', views.mark_incomplete_ticket, name='mark_incomplete_ticket'),
        path('main_queue', views.main_queue, name='main_queue'),
        path('waiting_list', views.waiting_list, name='waiting_list'),
        path('checkout_queue', views.checkout_queue, name='checkout_queue'),
        path('accept_ticket/<int:repairNumber>/',views.accept_ticket, name='accept_ticket'),
        path('repair_ticket/<int:repairNumber>/',views.repair_ticket,name='repair_ticket'),
        path('delete-ticket/<int:repairNumber>/',views.delete_ticket,name='delete_ticket'),
        path('checkout_ticket/<int:repairNumber>/',views.checkout_ticket,name='checkout_ticket'),
        path('enter_password/', views.enter_password, name='enter_password'),
        path('house_rules/', views.house_rules, name='house_rules'),
        path('change-category/<int:repairNumber>/', views.change_category, name='change_category'),
        path('checkout/<int:repairNumber>/',views.checkout,name='checkout'),
        path('checkout_success',views.checkout_success,name='checkout_success'),
        path('checkin_form/', views.checkin_form, name='checkin_form'),
        path('wait_for_accept/<int:repairNumber>/',views.wait_for_accept,name='wait_for_accept'),
        path('wait_for_checkout/<int:repairNumber>/',views.wait_for_checkout,name='wait_for_checkout'),

]
