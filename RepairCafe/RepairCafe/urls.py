from django.urls import path
from RepairCafe import views
from .views import enter_password

app_name = 'RepairCafe'

urlpatterns = [
        path('', views.index, name='index'),
        path('repair/<str:repairNumber>',views.repair_item,name='repair_item'),
        path('complete/<str:repairNumber>',views.complete_ticket,name='complete_ticket'),
        path('mark_incomplete_ticket/<str:repairNumber>/', views.mark_incomplete_ticket, name='mark_incomplete_ticket'),
        path('main_queue', views.main_queue, name='main_queue'),
        path('waiting_list', views.waiting_list, name='waiting_list'),
        path('accept_ticket/<str:repairNumber>/',views.accept_ticket, name='accept_ticket'),
        path('repair_ticket/<str:repairNumber>/',views.repair_ticket,name='repair_ticket'),
        path('delete-ticket/<str:repairNumber>/',views.delete_ticket,name='delete_ticket'),
        path('enter-password/', views.enter_password, name='enter_password'),

]
