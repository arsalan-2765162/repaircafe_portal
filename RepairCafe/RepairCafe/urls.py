from django.urls import path
from RepairCafe import views

app_name = 'RepairCafe'

urlpatterns = [
        path('', views.index, name='index'),
        path('main_queue', views.main_queue, name='main_queue'),
        path('waiting_list', views.waiting_list, name='waiting_list'),

]
