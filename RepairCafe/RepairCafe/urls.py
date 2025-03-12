from django.urls import include,path
from RepairCafe import views
from .views import enter_password
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = 'RepairCafe'

urlpatterns = [
        path('', views.index, name='index'),
	path('reset_data', views.reset_data, name='reset_data'),
        path('repair_item/<int:repairNumber>', views.repair_item, name='repair_item'),
        path('complete/<int:repairNumber>', views.complete_ticket, name='complete_ticket'),
        path('mark_incomplete_ticket/<int:repairNumber>', views.mark_incomplete_ticket, name='mark_incomplete_ticket'),
        path('main_queue', views.main_queue, name='main_queue'),
        path('waiting_list', views.waiting_list, name='waiting_list'),
        path('checkout_queue', views.checkout_queue, name='checkout_queue'),
        path('accept_ticket/<int:repairNumber>/', views.accept_ticket, name='accept_ticket'),
        path('repair_ticket/<int:repairNumber>/', views.repair_ticket, name='repair_ticket'),
        path('delete-ticket/<int:repairNumber>/', views.delete_ticket, name='delete_ticket'),
        path('checkout_ticket/<int:repairNumber>/', views.checkout_ticket, name='checkout_ticket'),
        path('ticket/<int:repairNumber>/pat-test/', views.pat_test, name='pat_test'),
        path('enter_password/', views.enter_password, name='enter_password'),
        path('house_rules/', views.house_rules, name='house_rules'),
        path('change-category/<int:repairNumber>/', views.change_category, name='change_category'),
        path('checkout/<int:repairNumber>/', views.checkout, name='checkout'),
        path('checkout_success',views.checkout_success, name='checkout_success'),
        path('checkin_form/', views.checkin_form, name='checkin_form'),
        path('wait_for_accept/<int:repairNumber>/', views.wait_for_accept, name='wait_for_accept'),
        path('wait_for_checkout/<int:repairNumber>/',  views.wait_for_checkout, name='wait_for_checkout'),
        path('repair_prompt/<int:repairNumber>/',  views.repair_prompt, name='repair_prompt'),
        path('wait_for_repair/<int:repairNumber>/', views.wait_for_repair, name='wait_for_repair'),
        path('repairer_login/', views.repairer_login, name='repairer_login'),
        path("repairer_logout/", views.repairer_logout, name="repairer_logout"),
        path('settings_page/', views.settings_page, name='settings_page'),
        path('basic_stats/', views.basic_stats,  name='basic_stats'),
        path('queue_position/<int:repairNumber>/', views.get_queue_position, name='queue_position'),
        path('volunteer_checkin/', views.volunteer_checkin, name='volunteer_checkin'),
        path('volunteer_checkin_success/<int:repairNumber>/', views.volunteer_checkin_success, name='volunteer_checkin_success'),
        path('volunteer_checkout/<int:repairNumber>/', views.volunteer_checkout, name='volunteer_checkout'),
        path('volunteer_checkout_success/', views.volunteer_checkout_success, name='volunteer_checkout_success'),
        path('admin/', admin.site.urls),
        path('admin_tools/', include('admin_tools.urls')),
        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
