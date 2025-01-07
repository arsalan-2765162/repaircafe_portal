from django.urls import path
from RepairCafe import views

app_name = 'RepairCafe'

urlpatterns = [
        path('', views.index, name='index'),
        path('repair/<str:repairNumber>',views.repair_item,name='repair_item'),
        path('complete/<str:repairNumber>',views.complete_ticket,name='complete_ticket'),
        path('main_queue', views.main_queue, name='main_queue'),
        path('waiting_list', views.waiting_list, name='waiting_list'),
        path('accept_ticket/<str:repairNumber>/',views.accept_ticket, name='accept_ticket'),
        path('repair_ticket/<str:repairNumber>/',views.repair_ticket,name='repair_ticket'),

]
