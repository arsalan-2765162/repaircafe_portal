from django.urls import path
from RepairCafe import views

app_name = 'RepairCafe'

urlpatterns = [
        path('', views.index, name='index'),
        path('queue/<slug:queue_name_slug>', views.view_queue, name='view_queue'),
]
