from django.urls import path
from RepairCafe import views

app_name = 'RepairCafe'

urlpatterns = [
        path('', views.index, name='index'),
        path('queue/<int:queue_id>/', views.view_queue, name='view_queue'),
]
