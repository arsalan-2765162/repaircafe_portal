from django.urls import path
from RepairCafe import views

app_name = 'RepairCafe'

urlpatterns = [
        path('', views.index, name='index')
]
